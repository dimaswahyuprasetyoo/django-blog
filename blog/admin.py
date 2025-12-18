from django.contrib import admin
from .models import Post, Comment

# --- KONFIGURASI ADMIN POST ---
class PostAdmin(admin.ModelAdmin):
    # Menampilkan kolom judul, kategori (SUDAH ADA DI MODEL), tanggal publish, dan author
    list_display = ('title', 'category', 'published_date', 'author')
    
    # Kotak pencarian
    search_fields = ('title', 'text')
    
    # Filter sidebar
    list_filter = ('category', 'published_date', 'author')
    
    date_hierarchy = 'published_date'
    ordering = ('-published_date',)

# --- KONFIGURASI ADMIN COMMENT ---
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'post', 'created_date', 'approved_comment')
    list_filter = ('approved_comment', 'created_date')
    search_fields = ('author', 'text')
    list_editable = ('approved_comment',)

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)