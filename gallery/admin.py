from django.contrib import admin
from .models import Photo, Profile

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_downloadable')  # 表示するカラムを指定
    search_fields = ('title',)  # タイトルで検索可能にする
    list_filter = ('is_downloadable',)  # ダウンロード可否でフィルター

admin.site.register(Photo, PhotoAdmin)  # Photoモデルにカスタム管理を適用
admin.site.register(Profile)  # Profileモデルはそのまま登録