from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError

from .models import User, Post, Tag, PostLike, Comment, CommentLike
import datetime
import markdown2


def index(request):
    if request.method == "POST" and request.user.is_authenticated:
        post = Post(user = request.user, title = request.POST["title"], content = request.POST["content"], time_stamp = datetime.datetime.utcnow())
        post.save()
        tags = request.POST["tags"].split(",")
        temp = []
        for tag in tags:
            tag = tag.strip().lower()
            if(tag not in temp and tag != ''):
                temp.append(tag)
        for tag in temp:
            t = Tag(post = post, content = tag)
            t.save()

    posts = Post.objects.all().order_by('-time_stamp')

    tags = Tag.objects.all()

    for post in posts:
        post.content = markdown2.markdown(post.content)

    if(request.user.is_authenticated):
        liked_posts = PostLike.objects.filter(user = request.user)
        liked_posts_id = []
        for post in posts:
            for liked_post in liked_posts:
                if(post.id == liked_post.post.id):
                    liked_posts_id.append(post.id)
                    break
        return render(request, "final_project/index.html",
            {
                "posts":posts,
                "liked_posts": liked_posts_id,
                "tags":tags,
            }
        )
    return render(request, "final_project/index.html",
        {
            "posts":posts,
            "tags":tags,
        }
    )


def login_view(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "final_project/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "final_project/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "final_project/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "final_project/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "final_project/register.html")


def liked_post(request, post_id):
    if(request.user.is_authenticated):
        try:
            post = Post.objects.get(pk = post_id)
            if(len(PostLike.objects.filter(user = request.user, post = post)) == 0):
                like = PostLike(user = request.user, post = post)
                post.likes+=1
                like.save()
                post.save()
            else:
                like = PostLike.objects.filter(user = request.user, post = post)
                post.likes-=1
                like.delete()
                post.save()

        except:
            pass
    return HttpResponse("")

def post(request, post_id):
    if(request.method == "POST" and request.user.is_authenticated):
        post = Post.objects.get(pk = post_id)
        comment = Comment(user = request.user, content = request.POST["content"], time_stamp = datetime.datetime.utcnow(), post = post)
        post.comments += 1
        comment.save()
        post.save()
        post.content = markdown2.markdown(post.content)
        liked_post = bool(len(PostLike.objects.filter(user = request.user, post = post).all()))
        tags = Tag.objects.filter(post = post)
        comments = Comment.objects.filter(post = post)
        for comment in comments:
            comment.content = markdown2.markdown(comment.content)
        liked_comments = CommentLike.objects.filter(user = request.user)
        liked_comments_id = []
        for comment in comments:
            for liked_comment in liked_comments:
                if(comment.id == liked_comment.comment.id):
                    liked_comments_id.append(comment.id)
                    break
        return render(request, "final_project/post.html",
            {
                "post":post,
                "liked_comments":liked_comments_id,
                "liked_post":liked_post,
                "tags":tags,
                "comments":comments,
            }
        )
    elif(request.user.is_authenticated):
        post = Post.objects.get(pk = post_id)
        post.content = markdown2.markdown(post.content)
        liked_post = bool(len(PostLike.objects.filter(user = request.user, post = post).all()))
        tags = Tag.objects.filter(post = post)
        comments = Comment.objects.filter(post = post)
        for comment in comments:
            comment.content = markdown2.markdown(comment.content)
        liked_comments = CommentLike.objects.filter(user = request.user)
        liked_comments_id = []
        for comment in comments:
            for liked_comment in liked_comments:
                if(comment.id == liked_comment.comment.id):
                    liked_comments_id.append(comment.id)
                    break
        print(post.likes)
        return render(request, "final_project/post.html",
            {
                "post":post,
                "liked_comments":liked_comments_id,
                "liked_post":liked_post,
                "tags":tags,
                "comments":comments,
            }
        )

def liked_comment(request, comment_id):
    if(request.user.is_authenticated):
        try:
            comment = Comment.objects.get(pk = comment_id)
            if(len(CommentLike.objects.filter(user = request.user, comment = comment)) == 0):
                like = CommentLike(user = request.user, comment = comment)
                comment.likes+=1
                like.save()
                comment.save()
            else:
                like = CommentLike.objects.filter(user = request.user, comment = comment)
                comment.likes-=1
                like.delete()
                comment.save()

        except:
            pass
    return HttpResponse("")

def search_by_tags(request):
    if(request.method == "POST"):
        tags = request.POST["tags"].split(",")
        final_tags = []
        for tag in tags:
            tag = tag.strip().lower()
            if(tag not in final_tags):
                final_tags.append(tag)
        posts = []
        for tag in final_tags:
            for post in Tag.objects.filter(content = tag):
                posts.append(post.post.id)
        final_posts = []
        for post in posts:
            if(post not in final_posts and posts.count(post) == len(final_tags)):
                final_posts.append(post)
        posts = []
        for post in final_posts:
            posts.append(Post.objects.get(pk = post))
        tags = Tag.objects.all()

        for post in posts:
            post.content = markdown2.markdown(post.content)
        posts.sort(key=lambda x: x.time_stamp, reverse=True)
        if(request.user.is_authenticated):
            liked_posts = PostLike.objects.filter(user = request.user)
            liked_posts_id = []
            for post in posts:
                for liked_post in liked_posts:
                    if(post.id == liked_post.post.id):
                        liked_posts_id.append(post.id)
                        break
            return render(request, "final_project/search_by_tags.html",
                {
                    "posts":posts,
                    "final_tags":final_tags,
                    "liked_posts": liked_posts_id,
                    "tags":tags,
                }
            )
        return render(request, "final_project/search_by_tags.html",
            {
                "posts":posts,
                "tags":tags,
                "final_tags":final_tags,
            }
        )
    elif(request.session.get("tag")):
        posts = []
        tag = request.session.get("tag")
        del request.session["tag"]
        for post in Tag.objects.filter(content = tag):
            post.post.content = markdown2.markdown(post.post.content)
            posts.append(post.post)
        tags = Tag.objects.all()

        posts.sort(key=lambda x: x.time_stamp, reverse=True)
        if(request.user.is_authenticated):
            liked_posts = PostLike.objects.filter(user = request.user)
            liked_posts_id = []
            for post in posts:
                for liked_post in liked_posts:
                    if(post.id == liked_post.post.id):
                        liked_posts_id.append(post.id)
                        break
            return render(request, "final_project/search_by_tags.html",
                {
                    "posts":posts,
                    "final_tag": tag,
                    "liked_posts": liked_posts_id,
                    "tags":tags,
                }
            )
        return render(request, "final_project/search_by_tags.html",
            {
                "posts":posts,
                "tags":tags,
                "final_tag":tag,
            }
        )
    return render(request, "final_project/search_by_tags.html")

def search_tag(request, tag):
    request.session["tag"] = tag.strip().lower()
    return HttpResponseRedirect(reverse("search_by_tags"))


def search_by_title(request):
    if(request.method == "POST"):
        title = request.POST["title"].lower()
        posts = []
        for post in Post.objects.all():
            if(title in post.title.lower()):
                posts.append(post)
        posts.sort(key=lambda x: x.time_stamp, reverse=True)
        for post in posts:
            post.content = markdown2.markdown(post.content)
        tags = Tag.objects.all()
        if(request.user.is_authenticated):
            liked_posts = PostLike.objects.filter(user = request.user)
            liked_posts_id = []
            for post in posts:
                for liked_post in liked_posts:
                    if(post.id == liked_post.post.id):
                        liked_posts_id.append(post.id)
                        break
            return render(request, "final_project/search_by_title.html",
                {
                    "posts":posts,
                    "title":title,
                    "liked_posts": liked_posts_id,
                    "tags":tags,
                }
            )
        return render(request, "final_project/search_by_title.html",
            {
                "posts":posts,
                "title":title,
                "tags":tags,
            }
        )

def edit_post(request, post_id):
    print(post_id)
    if(request.user.is_authenticated):
        if(request.method == "POST"):
            post = Post.objects.get(pk = post_id)
            tags = Tag.objects.filter(post = post)
            post.title = request.POST["title"]
            post.content = request.POST["content"]
            post.save()
            for tag in tags:
                tag.delete()
            tags = request.POST["tags"].split(",")
            temp = []
            for tag in tags:
                tag = tag.strip().lower()
                if(tag not in temp and tag != ''):
                    temp.append(tag)
            for tag in temp:
                t = Tag(post = post, content = tag)
                t.save()
            return HttpResponseRedirect(reverse("index"))

        post = Post.objects.get(pk = post_id)
        tags = Tag.objects.filter(post = post)

        print(post, tags)
        return render(request, "final_project/edit_post.html", {
            "post": post,
            "tags": tags,
        })

