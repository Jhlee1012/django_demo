from email.utils import decode_rfc2231
from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from .models import Post
from django.urls import reverse

# Create your views here.

def index(request):
  return HttpResponse(reverse('landing:home'))

def blog_home(request):
    blog_posts = Post.objects.all()
    context = {
        "blog_posts_key":blog_posts,
    }
    return render(request,'blog/index.html',context)

def blog_post_write(request):
 if request.method == "GET":
     return render(request,'blog/create.html')
 if request.method == "POST":
     new_post = Post()
     new_post.title = request.POST["title"]
     new_post.content = request.POST["content"]
     if request.FILES.get("image"):
         new_post.head_image = request.FILES["image"]
     new_post.save()
     return HttpResponseRedirect(reverse("blog:home"))

def blog_post_view(request,post_id):
    try :
        a_post = Post.objects.get(id=post_id)
        context ={
        "id":a_post.id,
        "title" : a_post.title, 
        "content" : a_post.content,
        "head_image" :a_post.head_image
        }
        return render(request,'blog/details.html',context)
    except : 
        raise Http404()

def blog_post_update(request,post_id):
    a_post = Post.objects.get(id=post_id)
    context ={
        "id":a_post.id,
        "title" : a_post.title, 
        "content" : a_post.content,
    }
   
    if request.method == "GET":
        return render(request,'blog/edit.html',context)

    if request.method == "POST":
        a_post.title = request.POST["title"]
        a_post.content = request.POST["content"]
        a_post.save()
        return HttpResponseRedirect(reverse("blog:detail",args=[a_post.id]))

def blog_post_delete(request,post_id):
    if request.method == "POST" :
        a_post = Post.objects.get(id = post_id)
        a_post.delete()
        return HttpResponseRedirect(reverse("blog:home"))
