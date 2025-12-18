from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse

# --- BAGIAN POSTINGAN (LIST & DETAIL) ---

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

# --- BAGIAN ADMIN (NEW & EDIT DENGAN UPLOAD GAMBAR) ---

@login_required
def post_new(request):
    if request.method == "POST":
        # request.FILES wajib ada untuk upload gambar
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        # request.FILES wajib ada untuk update gambar
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form, 'post': post})

# --- BAGIAN KOMENTAR (ADD, REPLY, REMOVE) ---

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form, 'post': post})

# Fungsi ini yang menyebabkan error karena sebelumnya hilang
@login_required
def remove_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)

def reply_to_comment(request, pk):
    parent_comment = get_object_or_404(Comment, pk=pk)
    post = parent_comment.post
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.post = post
            reply.parent = parent_comment 
            reply.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    
    return render(request, 'blog/add_comment_to_post.html', {
        'form': form, 
        'post': post, 
        'parent_comment': parent_comment
    })

# --- BAGIAN REACTION (LIKE, LOVE, DLL) ---

def react_to_comment(request, pk, reaction_type):
    # Hanya menerima request AJAX/JSON
    comment = get_object_or_404(Comment, pk=pk)
    
    # Cek Cookies agar tidak spam
    cookie_name = f'reacted_{pk}'
    if request.COOKIES.get(cookie_name):
        return JsonResponse({'status': 'error', 'message': 'Anda sudah bereaksi!'}, status=400)

    # Increment sesuai tipe
    if reaction_type == 'like':
        comment.reaction_like += 1
    elif reaction_type == 'love':
        comment.reaction_love += 1
    elif reaction_type == 'haha':
        comment.reaction_haha += 1
    elif reaction_type == 'wow':
        comment.reaction_wow += 1
    elif reaction_type == 'sad':
        comment.reaction_sad += 1
    elif reaction_type == 'angry':
        comment.reaction_angry += 1
    else:
        return JsonResponse({'status': 'error'}, status=400)
    
    comment.save()
    
    new_count = getattr(comment, f'reaction_{reaction_type}')
    
    response = JsonResponse({
        'status': 'success', 
        'new_count': new_count,
        'type': reaction_type
    })
    
    response.set_cookie(cookie_name, 'true', max_age=31536000)
    return response

# --- BAGIAN LOGOUT ---

def custom_logout(request):
    logout(request)
    return redirect('/')