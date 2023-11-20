from django.utils import timezone
from django.db import transaction

from rest_framework import serializers
from rest_framework.fields import HiddenField, CurrentUserDefault
from user_app.models import UserProfile, FavouritePlayers, UserBetPaymentInfo, ReportType, ReportUser
# from notifications_app.tasks import send_push_task
# from feeds_app.serializers import FeedVideoSerializer
# from game_app.models import Game


class UserNotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['pk']


class UserBetPaymentInfoSerializer(serializers.ModelSerializer):
    owner = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = UserBetPaymentInfo
        exclude = ['created_at', 'updated_at']
        read_only_fields = ['user', ]

    def validate(self, attrs):
        user = attrs.pop('owner').userprofile
        # if UserBetPaymentInfo.objects.filter(user=user, payment_method_name=attrs['payment_method_name']).exists():
        #     raise serializers.ValidationError({'payment_method_name':'Provided payment method name already existed for user'})
        attrs['user'] = user
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    age = serializers.IntegerField(read_only=True)
    role = serializers.CharField(required=False)
    is_social_login = serializers.BooleanField(read_only=True)
    payment_method_name = serializers.CharField(required=False)
    payment_method_url = serializers.CharField(required=False)

    # payment_details = serializers.SerializerMethodField(required=False,read_only=True)
    # payment_details = UserBetPaymentInfoSerializer(many=True,allow_null=True,source="bet_payments_info")

    # def get_payment_details(self,obj):
    #     objs = obj.bet_payments_info.all()
    #     return UserBetPaymentInfoSerializer(objs, many=True).data

    class Meta:
        model = UserProfile
        exclude = ['created_at', 'updated_at', 'active', 'user']

    def validate(self, attrs):
        print("inside validate")
        print(attrs)
        dob = attrs.get('dob')
        if dob:
            if dob > timezone.now().date():
                raise serializers.ValidationError({'dob': 'Cannot enter date ahead of current date'})
        return attrs

    def update(self, instance, validated_data):
        with transaction.atomic():
            payment_method_name = validated_data.pop('payment_method_name', None)
            payment_method_url = validated_data.pop('payment_method_url', None)
            super(UserProfileSerializer, self).update(self.instance, self.validated_data)

            if payment_method_name and payment_method_url:
                UserBetPaymentInfo.objects.create(
                    payment_method_name=payment_method_name,
                    payment_method_url=payment_method_url,
                    user=self.instance
                )

            return instance

    # def save(self, **kwargs):
    #     with transaction.atomic():
    #         # payment_details = self.validated_data.pop('bet_payments_info',None)
    #         payment_method_name = self.validated_data.pop('payment_method_name',None)
    #         payment_method_url = self.validated_data.pop('payment_method_url',None)
    #         super(UserProfileSerializer,self).update(self.instance,self.validated_data)
    #         # if payment_details:
    #         #     # UserBetPaymentInfoSerializer
    #         #     print("inside payment details : ", payment_details)
    #         #     print(payment_details)
    #         #     UserBetPaymentInfo.objects.create(
    #         #         **payment_details,
    #         #         user=self.instance
    #         #     )
    #
    #         if payment_method_name and payment_method_url:
    #             UserBetPaymentInfo.objects.create(
    #                 payment_method_name=payment_method_name,
    #                 payment_method_url=payment_method_url,
    #                 user=self.instance
    #             )
    #
    #             self.validated_data.update({
    #                     'payment_method_name':payment_method_name,
    #                     'payment_method_url':payment_method_url
    #             })
    #
    # # TODO: payment_method_name and payment_method_url not being returned
    # # def to_representation(self, instance):
    # #     data = super(UserProfileSerializer, self).to_representation(instance)
    # #     # data['payment_method_name'] = self.validated_data.get('payment_method_name')
    # #     # data['payment_method_url'] = self.validated_data.get('payment_method_url')
    # #
    # #     return data


# This serializer is being used to return player profile when game is creating
class GamePlayerProfileSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'full_name', 'image']  # 'email',


class FavouritePlayersSerializer(serializers.ModelSerializer):
    owner = HiddenField(default=CurrentUserDefault())
    full_name = serializers.CharField(read_only=True, source="favourite_player.full_name")
    image = serializers.CharField(read_only=True, source="favourite_player.image")

    class Meta:
        model = FavouritePlayers
        fields = '__all__'
        read_only_fields = ['active', 'followed_by']

    def create(self, validated_data):
        owner_profile = validated_data.pop('owner')
        obj = FavouritePlayers.objects.create(**validated_data, followed_by=owner_profile.userprofile)
        favourite_player = validated_data['favourite_player']
        send_push_task.delay(
            title="You have a new Homie",
            message="{} has marked you as Homie".format(owner_profile.userprofile.full_name),
            user=favourite_player.id,
            ref_id=owner_profile.id,
            noti_type="NEW_HOMIE",
            data={},
            allow_notifications=favourite_player.allow_notifications
        )
        return obj

    def validate(self, attrs):
        owner_profile = attrs['owner'].userprofile
        if owner_profile == attrs['favourite_player']:
            raise serializers.ValidationError('Cannot mark yourself as homie')

        if FavouritePlayers.objects.filter(favourite_player=attrs['favourite_player'], followed_by=owner_profile).exists():
            raise serializers.ValidationError('You have already marked this user as homie')

        # if self.instance:
        #     print("self.instance.followed_by : ", self.instance.followed_by)
        #     print("owner_profile : ", owner_profile)
        #     if self.instance.followed_by != owner_profile:
        #         raise serializers.ValidationError("Only follower can unfollow homie")

        return attrs

    # def to_representation(self, instance):
    #     data = super(FavouritePlayersSerializer, self).to_representation(instance)
    #     data['favourite_player_name'] = instance.favourite_player.full_name
    #     data['favourite_player_image'] = instance.favourite_player.image
    #     return data


class ReportTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportType
        exclude = ['created_at', 'updated_at']
        read_only_fields = ['active']


class ReportSerializer(serializers.ModelSerializer):
    owner = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = ReportUser
        exclude = ['created_at', 'updated_at']
        read_only_fields = ['active', 'reportee']

    def validate(self, attrs):
        owner_profile = attrs.pop('owner').userprofile
        if owner_profile == attrs['reported']:
            raise serializers.ValidationError('Cannot report yourself')
        attrs['reportee'] = owner_profile

        if ReportUser.objects.filter(**attrs).exists():
            raise serializers.ValidationError('You have already reported this user for selected type')

        return attrs

    def create(self, validated_data):
        print("validated data : ", validated_data)
        # owner_profile = validated_data.pop('owner')
        obj = ReportUser.objects.create(**validated_data)

        return obj


class MyBetsSerializer(serializers.Serializer):
    bets_placed = serializers.IntegerField(read_only=True)
    bets_won = serializers.IntegerField(read_only=True)
    bets_lost = serializers.IntegerField(read_only=True)

    def to_representation(self, instance):
        print("inside to repr")
        # print()

        data = super(MyBetsSerializer, self).to_representation(instance)
        print("data : ", data)
        # data['favourite_player_name'] = instance.favourite_player.full_name
        # data['favourite_player_image'] = instance.favourite_player.image
        return data


# TODO: resolve circular dependency issue
# from game_app.serializers import MatchesHistoryUserProfileSerializer


class MyProfileSerializer(serializers.ModelSerializer):
    videos = serializers.SerializerMethodField()
    matches_history = serializers.SerializerMethodField()
    payment_info = serializers.SerializerMethodField()
    is_already_homie = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserProfile
        exclude = ['created_at', 'updated_at', 'active']

    def get_is_already_homie(self, obj):
        value = False
        owner = self.context['request'].user.userprofile
        homie = owner.favourite_player.filter(favourite_player=obj)
        if homie:
            value = True
        return value

    def get_videos(self, obj):
        user_videos = obj.video_set.filter(active=True).order_by('-id')[:2]
        return FeedVideoSerializer(user_videos, many=True, context={'request': self.context['request']}).data

    def get_matches_history(self, obj):
        user_games = Game.objects.filter(gameplayers__player=obj, game_status__in=('S', 'E')).order_by('-id')[:2]
        return MatchesHistoryUserProfileSerializer(user_games, many=True, context={'owner': obj}).data

    def get_payment_info(self, obj):
        objs = obj.bet_payments_info.all()
        return UserBetPaymentInfoSerializer(objs, many=True).data

# class MyScorecardsSerializer(serializers.Serializer):
#     # user = UserProfileSerializer(read_only=True)
#     videos = serializers.SerializerMethodField()
#     matches_history = serializers.SerializerMethodField()
#
#     def get_videos(self, obj):
#         return FeedVideoSerializer(obj.video_set.all(),many=True).data
#
#     def get_matches_history(self,obj):
#         user_games = Game.objects.filter(gameplayers__player=obj,game_status='E')
#         return MatchesHistorySerializer(user_games, many=True, context={'owner': obj}).data
