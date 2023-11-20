import jwt

from django.conf import settings
from django.contrib.auth import get_user_model, password_validation
from django.utils import timezone

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.fields import HiddenField, CurrentUserDefault

from auth_app.models import UserOtp
from user_app.models import UserProfile
from user_app.serializers import UserProfileSerializer
from auth_app.tasks import send_otp_registration, send_welcome_email
from django.db.models import Q


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    mobile_number = serializers.CharField(required=False,write_only=True)
    first_name = serializers.CharField(required=False,write_only=True)
    last_name = serializers.CharField(required=False,write_only=True)
    password = serializers.CharField(write_only=True, required=True,validators=[password_validation.validate_password])
    device_token = serializers.CharField(write_only=True, required=False, allow_blank=True)
    device_type = serializers.CharField(write_only=True)
    image = serializers.ImageField(required=False)
    city = serializers.CharField(required=False)
    state = serializers.CharField(required=False)
    zipcode = serializers.IntegerField(required=False)
    gender = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('email', 'password', 'mobile_number', 'first_name', 'last_name', 'device_token', 'device_type', 'image', 'city', 'state', 'zipcode', 'gender')

    def validate(self, attrs):
        if User.objects.filter(email=attrs['email'].lower()).exists():
            raise serializers.ValidationError({"email": "Email already exists."})
        return attrs
    # def validate(self, attrs):
    #     if attrs['password1'] != attrs['password2']:
    #         raise serializers.ValidationError({"password": "Password fields didn't match."})
    #     return attrs

    def create(self, validated_data):
        print(validated_data)

        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            mobile_number=validated_data.get('mobile_number'),
            image=validated_data.get('image'),
            city=validated_data.get('city'),
            state=validated_data.get('state'),
            zipcode=validated_data.get('zipcode'),
            gender=validated_data.get('gender')
        )

        # sending email via celery
        code = UserOtp.generate_otp(user.id)
        #TODO: send email via celery
        send_otp_registration(code, user.email)

        # TODO: move this to RegistrationOtpVerificationSerializer save's method
        # adding user device token and type in FCMDevice model to use it when sending notification
        # FCMDevice.objects.create(
        #     registration_id=validated_data.get('device_token'),
        #     type=validated_data.get('device_type'),
        #     user_id=user.id
        # )

        #TODO: send email via celery
        send_welcome_email(validated_data.get('full_name'), user.email)

        return user

    def to_representation(self, instance):
        data = super(RegisterSerializer, self).to_representation(instance)
        data['full_name'] = f"{instance.first_name} {instance.last_name}"
        data['mobile_number'] = str(instance.userprofile.mobile_number)
        return data


class RegistrationOtpVerificationSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=7, min_length=4, required=True, write_only=True,
                                 help_text="OTP sent to your email")
    email = serializers.CharField(write_only=True, required=True)
    is_verified = serializers.BooleanField(read_only=True)
    token = serializers.CharField(read_only=True)
    user_details = UserProfileSerializer(required=False, read_only=True)


    def validate(self, attrs):
        attrs['user'] = User.get_or_none(email=attrs['email'])
        if not attrs['user']:
            raise serializers.ValidationError({"email": "User with this email does not exist."})
        if UserOtp.verify_otp(code=attrs['code'], user__id=attrs['user'].id):
            attrs['user'].is_verified = True
            attrs['user'].save()
            attrs['user_details'] = attrs['user'].userprofile  # this is to return details of logged in user
            return attrs

        raise serializers.ValidationError({"code": "Invalid OTP or Expired OTP"})

    def save(self, **kwargs):
        user = self.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        utc_now = timezone.now()
        # device_token = self.validated_data.get('device_token')

        # TODO: will frontend send a device token in verification aswell?
        # if not created and token.created < (utc_now - settings.AUTH_TOKEN_EXPIRATION):
        if not created:
            # if (token.created < (utc_now - settings.AUTH_TOKEN_EXPIRATION)) or (device_token != user.device_token):
            if (token.created < (utc_now - settings.AUTH_TOKEN_EXPIRATION)):
                # print("new device_token is not same as old one therefore creating new token")
                token.delete()
                token = Token.objects.create(user=user)
                token.created = utc_now
                token.save()

                # user.device_token = device_token
                # user.save()
        return self.validated_data.update({'is_verified': True, 'token': token.key})


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)
    device_token = serializers.CharField(write_only=True, required=False, allow_blank=True)
    device_type = serializers.CharField(write_only=True)
    user_details = UserProfileSerializer(required=False, read_only=True)
    is_verified = serializers.BooleanField(read_only=True)


    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = User.get_or_none(email=email)
        is_verified = True
        if user is None:
            raise serializers.ValidationError({"email": "User with this email does not exist."})
        if not user.is_verified:
            is_verified = False

            # raise serializers.ValidationError({"is_verified": "User is not verified"})
        if not user.check_password(password):
            raise serializers.ValidationError({"password": "Incorrect password."})
        if not user.is_active:
            raise serializers.ValidationError({"email": "User is not active."})

        attrs['is_verified'] = is_verified
        attrs['user_details'] = user.userprofile # this is to return details of logged in user

        device_token = attrs.get('device_token')
        device_type = attrs.get('device_type')
        user_profile = user.userprofile
        attrs['token'], created = Token.objects.get_or_create(user=user)
        # user_fcm = user.fcmdevice_set.all()

        # if user_fcm:
        #     user_fcm = user_fcm.first()
        #     if device_token != user_fcm.registration_id or device_type != user_fcm.type:
        #         # if device_token == '':
        #         #     user_fcm.delete()
        #         # else:
        #         user_fcm.registration_id = device_token
        #         user_fcm.type = device_type
        #         user_fcm.save()

        #         Token.objects.filter(user=user).delete()
        #         attrs['token'] = Token.objects.create(user=user)
        #     else:
        #         attrs['token'], created = Token.objects.get_or_create(user=user)
        # else:
        #     # if device_token != '':
        #     FCMDevice.objects.create(
        #         registration_id=device_token,
        #         type=device_type,
        #         user_id=user.id
        #     )
        #     Token.objects.filter(user=user).delete()
        #     attrs['token'] = Token.objects.create(user=user)

        attrs['user_details'] = user_profile # this is to return details of logged in user
        return attrs

    def save(self, **kwargs):
        token = self.validated_data.get("token")
        if self.validated_data['is_verified']:
            return self.validated_data.update({'token': token.key})
        return self.validated_data.update({'token': ''})


class LogoutSerializer(serializers.Serializer):
    success = serializers.BooleanField(read_only=True)

    def save(self, request, **kwargs):
        user = request.user
        request.user.auth_token.delete()
        return None


class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    success = serializers.BooleanField(read_only=True, default=True)
    message = serializers.CharField(read_only=True, default="OTP sent successfully")

    def validate(self, attrs):
        attrs['user'] = User.get_or_none(email=attrs['email'])
        if not attrs['user']:
            raise serializers.ValidationError({"email": "User with this email does not exist."})
        return attrs

    def save(self, **kwargs):
        user = self.validated_data['user']
        code = UserOtp.generate_otp(user.id)
        if UserOtp.send_otp(user.email, code):
            return self.validated_data
        raise serializers.ValidationError("OTP sending failed")


class OtpVerificationSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=7, min_length=4, required=True, write_only=True,
                                 help_text="OTP sent to your email")
    email = serializers.CharField(write_only=True, required=True)
    token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        attrs['user'] = User.get_or_none(email=attrs['email'])
        if not attrs['user']:
            raise serializers.ValidationError({"email": "User with this email does not exist."})
        if UserOtp.verify_otp(code=attrs['code'], user__id=attrs['user'].id):
            return attrs
        raise serializers.ValidationError({"code": "Invalid OTP or Expired OTP"})

    def save(self, **kwargs):
        user = self.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return self.validated_data.update({'token': token.key})


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True, write_only=True,
                                         validators=[password_validation.validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)
    token = serializers.CharField(read_only=True)
    owner = HiddenField(default=CurrentUserDefault())

    # success = serializers.BooleanField(read_only=True, default=True)
    # message = serializers.CharField(read_only=True, default="Password reset successfully")

    def save(self, request):
        owner = self.validated_data.pop('owner')
        owner.auth_token.delete()
        owner.set_password(self.validated_data['new_password'])
        owner.save()
        token = Token.objects.create(user=request.user)
        self.validated_data.update({'token': token.key})
        return None

    def validate(self, attrs):
        owner = attrs['owner']
        if owner.check_password(attrs['new_password']):
            raise serializers.ValidationError({'password': "You have entered an old password, kindly use a new one"})
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "The passwords donot match."})
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(required=True, write_only=True,
                                         validators=[password_validation.validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)
    token = serializers.CharField(read_only=True)
    owner = HiddenField(default=CurrentUserDefault())

    def save(self, request):
        owner = self.validated_data.pop('owner')
        owner.auth_token.delete()
        owner.set_password(self.validated_data['new_password'])
        owner.save()
        token = Token.objects.create(user=request.user)
        self.validated_data.update({'token': token.key})
        return None

    def validate(self, attrs):
        owner = attrs['owner']
        if not owner.check_password(attrs['old_password']):
            raise serializers.ValidationError({'password': "Old password donot match."})

        if owner.check_password(attrs['new_password']):
            raise serializers.ValidationError({'password': "You have entered an old password, kindly use a new one"})

        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "The passwords donot match."})
        return attrs


class SocialLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False,write_only=True)
    name = serializers.CharField(required=False,write_only=True)
    provider = serializers.ChoiceField(required=False,choices=['AP','FB','GO'])
    platform_token = serializers.CharField(write_only=True) # this indicate the unique id for all 3 social logins, in case of apple login key 'sub' is being returned in it
    apple_token = serializers.CharField(write_only=True, required=False) # contains jwt token which is decoded and email is extracted form it
    token = serializers.CharField(read_only=True)

    device_token = serializers.CharField(write_only=True, required=False, allow_blank=True)
    device_type = serializers.CharField(write_only=True)
    user_details = UserProfileSerializer(required=False, read_only=True)


    def validate(self, attrs):
        email = attrs.get('email')
        user = User.get_or_none(email=attrs.get('email'))
        name = attrs.get('name')
        platform_token = attrs.get('platform_token')
        device_token = attrs.get('device_token')
        device_type = attrs.get('device_type')
        provider = attrs.get('provider')

        # means request is initiated for registration
        if user is None:
            if attrs.get('provider') == 'AP':
                try:
                    decoded_token = jwt.decode(attrs.get('apple_token'), options={"verify_signature": False})
                    email = decoded_token['email']
                except Exception as e:
                    raise serializers.ValidationError({'platform_token': 'Invalid token'})

            user = User.objects.create(email=email
                                       ,is_social_login=True
                                       # ,device_token=device_token
                                       # ,device_type=attrs.get('device_type')
                                       ,platform_token=platform_token
                                       ,provider=attrs.get('provider')
                                       ,is_verified=True
                                    )
            user_profile = UserProfile.objects.create(
                full_name=name,
                user=user
            )

            attrs['token'] = Token.objects.create(user=user)

            if device_token:
                FCMDevice.objects.create(
                    registration_id=device_token,
                    type=device_type,
                    user_id=user.id
                )
        else:
            # check for platform
            if user.provider != provider:
                raise serializers.ValidationError({'provider': f'You are already logged in from: {user.get_provider_display()}'})

            print("user already existed")
            user_profile = user.userprofile
            user_fcm = user.fcmdevice_set.all()
            if user_fcm:
                user_fcm = user_fcm.first()
                if device_token != user_fcm.registration_id or device_type != user_fcm.type:
                    # if device_token == '':
                    #     user_fcm.delete()
                    # else:
                    user_fcm.registration_id = device_token
                    user_fcm.type = device_type
                    user_fcm.save()

                    Token.objects.filter(user=user).delete()
                    attrs['token'] = Token.objects.create(user=user)
                else:
                    attrs['token'], created = Token.objects.get_or_create(user=user)
            else:
                # if device_token != '':
                FCMDevice.objects.create(
                    registration_id=device_token,
                    type=device_type,
                    user_id=user.id
                )
                Token.objects.filter(user=user).delete()
                attrs['token'] = Token.objects.create(user=user)

        attrs['user_details'] = user_profile # this is to return details of logged in user
        return attrs


    def save(self, **kwargs):
        token = self.validated_data.get("token")
        return self.validated_data.update({'token': token.key})