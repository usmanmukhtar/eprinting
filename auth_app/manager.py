from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email=None, password=None, *args,**kwargs):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            # email=self.normalize_email(email),
            email=email.lower(),
        )
        user.set_password(password)
        user.save(using=self._db)
        user.create_user_profile(**kwargs)
        return user

    def create_superuser(self, email, password, *args, **kwargs):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user