from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, phone_number, invite_code=None):
        if not phone_number:
            raise ValueError('Необходимо указать номер телефона!')
        user = self.model(phone_number=phone_number)
        user.invite_code = invite_code
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password):
        user = self.create_user(phone_number)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
