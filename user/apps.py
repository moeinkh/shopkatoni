from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'user'
    verbose_name = 'پروفایل کاربران'

    def ready(self):
        import user.signal