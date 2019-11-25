from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import Signal

from .utilities import send_activation_notification, get_timestamp_path

user_registrated = Signal(providing_args=['instance'])Ваше місцезнаходження


def user_registrated_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])


user_registrated.connect(user_registrated_dispatcher)


class ProfileUser(AbstractUser):
    """Create model for registered users."""
    is_activated = models.BooleanField(default=True, db_index=True,
                                       verbose_name='Прошел активацию?')
    send_messages = models.BooleanField(default=True,
                        verbose_name='Слать оповещения о новых комментариях?')
    date_of_birth = models.DateField(blank=True, null=True)

    def delete(self, *args, **kwargs):
        for np in self.np_set.all():
            np.delete()
        super().delete(*args, **kwargs)


class Meta(AbstractUser.Meta):
    pass


class NewsPost(models.Model):

    title = models.CharField(max_length=40, verbose_name='Новость')

    is_approved = models.BooleanField(default=False, db_index=True,
                                      verbose_name='Одобренный пост')
    image = models.ImageField(blank=True, upload_to=get_timestamp_path,
                              verbose_name='Изображение')

    content = models.TextField(verbose_name='Текст новости')

    author = models.ForeignKey(ProfileUser, on_delete=models.CASCADE,
                               verbose_name='Автор новости')

    is_active = models.BooleanField(default=True, db_index=True,
                                    verbose_name='Выводить в списке?')

    created_at = models.DateTimeField(auto_now_add=True, db_index=True,
                                      verbose_name='Опубликовано')

    def delete(self, *args, **kwargs):
        for ai in self.additionalimage_set.all():
            ai.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Новости'
        verbose_name = 'Новость'
        ordering = ['-created_at']


class AdditionalImage(models.Model):
    np = models.ForeignKey(NewsPost, on_delete=models.CASCADE,
                           verbose_name='Новость')
    image = models.ImageField(upload_to=get_timestamp_path,
                              verbose_name='Изображение')

    class Meta:
        verbose_name_plural = 'Дополнительные иллюстрации'
        verbose_name = 'Дополнительная иллюстрация'
