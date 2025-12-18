from django.db import models
from django.conf import settings
from django.utils import timezone
from tinymce.models import HTMLField 

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    
    # --- FIELD YANG HILANG KITA KEMBALIKAN ---
    category = models.CharField(max_length=100, default='Umum')

    # Field Rich Text Editor (TinyMCE)
    text = HTMLField()
    
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    
    # Field Gambar Header
    header_image = models.ImageField(upload_to='post_images/', blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    # Reaction Fields
    reaction_like = models.PositiveIntegerField(default=0)
    reaction_love = models.PositiveIntegerField(default=0)
    reaction_haha = models.PositiveIntegerField(default=0)
    reaction_wow = models.PositiveIntegerField(default=0)
    reaction_sad = models.PositiveIntegerField(default=0)
    reaction_angry = models.PositiveIntegerField(default=0)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text