from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'header_image',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Style Input Judul (Glass Effect)
        self.fields['title'].widget.attrs.update({
            'class': 'form-control',
            'style': 'background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.2); color: white; border-radius: 10px; padding: 10px;',
            'placeholder': 'Masukkan Judul Berita...'
        })
        
        # Style Input Konten (Glass Effect)
        self.fields['text'].widget.attrs.update({
            'class': 'form-control',
            'style': 'background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.2); color: white; height: 300px; border-radius: 10px; padding: 10px;',
            'placeholder': 'Tulis isi berita di sini...'
        })

        # Style Upload Gambar
        self.fields['header_image'].widget.attrs.update({
            'class': 'form-control',
            'style': 'background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); color: white; border-radius: 10px;'
        })

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text',)