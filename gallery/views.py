from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import EmailMessage
from django.core.files.base import ContentFile
from PIL import Image as PILImage
import io

from .models import Photo, Profile
from .forms import ContactForm, PhotoForm

def gallery_view(request):
    query = request.GET.get('q')
    if query:
        photos = Photo.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    else:
        photos = Photo.objects.all()
    return render(request, 'gallery/gallery.html', {'photos': photos, 'query': query})

def profile_view(request):
    profile = Profile.objects.first()
    return render(request, 'gallery/profile.html', {'profile': profile})

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            try:
                email_message = EmailMessage(
                    subject=f'Message from {name}',
                    body=message,
                    from_email='loadingnowak@gmail.com',
                    to=['loadingnowak@gmail.com'],
                )
                email_message.reply_to = [email]
                email_message.send(fail_silently=False)
                messages.success(request, 'Your message has been sent successfully.')
                return redirect('contact_success')
            except Exception as e:
                messages.error(request, f'An error occurred: {e}')
    else:
        form = ContactForm()
    return render(request, 'gallery/contact.html', {'form': form})

def contact_success(request):
    return render(request, 'gallery/contact_success.html')

@login_required
def upload_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gallery')
    else:
        form = PhotoForm()
    return render(request, 'gallery/upload_photo.html', {'form': form})

@login_required
def preview_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_photo = form.cleaned_data['image']
            return render(request, 'gallery/preview_photo.html', {'uploaded_photo': uploaded_photo})
    else:
        form = PhotoForm()
    return render(request, 'gallery/upload_photo.html', {'form': form})

@login_required
def download_photo(request, photo_id):
    photo = Photo.objects.get(id=photo_id)
    if photo.is_downloadable:
        image_path = photo.image.path
        with open(image_path, 'rb') as img_file:
            response = HttpResponse(img_file.read(), content_type='image/jpeg')
            response['Content-Disposition'] = f'attachment; filename="{photo.title}.jpg"'
            return response
    else:
        return HttpResponse("ダウンロードは許可されていません。")

@login_required
def show_photo(request, photo_id):
    photo = Photo.objects.get(id=photo_id)
    if photo.is_downloadable:
        img = PILImage.open(photo.image.path)
        img.thumbnail((400, 400))
        img_io = io.BytesIO()
        img.save(img_io, format='JPEG')
        img_file = ContentFile(img_io.getvalue(), name=f"{photo.title}_small.jpg")
        return render(request, 'gallery/show_photo.html', {'photo': photo, 'small_image': img_file})
    else:
        return HttpResponse("表示は許可されていません。")

# スーパーユーザー用のデコレータ
def superuser_required(view_func):
    def check_superuser(user):
        return user.is_superuser
    return user_passes_test(check_superuser)(view_func)

@superuser_required
def edit_photo(request, photo_id):
    try:
        photo = get_object_or_404(Photo, id=photo_id)
        if request.method == 'POST':
            form = PhotoForm(request.POST, request.FILES, instance=photo)
            if form.is_valid():
                form.save()
                return redirect('gallery')
        else:
            form = PhotoForm(instance=photo)
        return render(request, 'gallery/edit_photo.html', {'form': form, 'photo': photo})
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}")

@superuser_required
def delete_photo(request, photo_id):
    try:
        photo = get_object_or_404(Photo, id=photo_id)
        if request.method == 'POST':
            photo.delete()
            return redirect('gallery')
        return render(request, 'gallery/delete_photo.html', {'photo': photo})
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}")
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('gallery')  # ギャラリーページにリダイレクト