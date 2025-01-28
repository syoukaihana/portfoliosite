from django.db import models
from PIL import Image
import os
from django.conf import settings

class Photo(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='photos/')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_downloadable = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        max_size = (800, 800)
        img.thumbnail(max_size)
        img.save(self.image.path)

    def delete(self, *args, **kwargs):
        # 画像ファイルを削除
        if self.image:
            # media/photoディレクトリからの画像パスを取得
            photo_path = os.path.join(settings.MEDIA_ROOT, self.image.name)
            if os.path.isfile(photo_path):
                os.remove(photo_path)  # メディアファイルを削除
        super().delete(*args, **kwargs)  # モデルを削除

class Profile(models.Model):
    user_name = models.CharField(max_length=100)
    bio = models.TextField()
    profile_image = models.ImageField(upload_to='profiles/', blank=True)

    def __str__(self):
        return self.user_name
