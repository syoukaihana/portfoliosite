from django.urls import path
from .views import (
    gallery_view,
    profile_view,
    contact_view,
    contact_success,
    upload_photo,
    preview_photo,
    download_photo,
    show_photo, edit_photo, delete_photo, # 追加
    
)
from gallery.views import logout_view

urlpatterns = [
    path('', gallery_view, name='gallery'),
    path('profile/', profile_view, name='profile'),
    path('contact/', contact_view, name='contact'),
    path('contact/success/', contact_success, name='contact_success'),
    path('upload/', upload_photo, name='upload_photo'),
    path('preview/', preview_photo, name='preview_photo'),
    path('download/<int:photo_id>/', download_photo, name='download_photo'),
    path('show/<int:photo_id>/', show_photo, name='show_photo'),  # 追加
    path('edit/<int:photo_id>/', edit_photo, name='edit_photo'),  # 画像編集用のURL
    path('delete/<int:photo_id>/', delete_photo, name='delete_photo'),  # 画像削除用のURL
    path('accounts/logout/', logout_view, name='logout'),
]
