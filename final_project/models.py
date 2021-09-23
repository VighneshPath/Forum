from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "posts")

    title = models.CharField(max_length = 128)

    content = models.TextField()

    time_stamp = models.DateTimeField(auto_now = False, auto_now_add = True)

    likes = models.IntegerField(default = 0)

    comments = models.IntegerField(default = 0)

    def __str__(self):
        return f"By: {self.user}\nContent: {self.content}\nPosted: {self.time_stamp}\nLikes: {self.likes}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = "comment")

    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "commenter")

    content = models.TextField()

    time_stamp = models.DateTimeField(auto_now = False, auto_now_add = True)

    likes = models.IntegerField(default = 0)

    def __str__(self):
        return f"By: {self.user}\nContent: {self.content}\nPosted: {self.time_stamp}\nLikes: {self.likes}\nOn Post: {self.post}"


class Tag(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = "tags")

    content = models.TextField()

    def __str__(self):
        return f"Post: {self.post}\nTag: {self.content}"


class PostLike(models.Model):

    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "liked_by_post")
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = "liked_post")

    def __str__(self):
        return f"{self.user} Liked {self.post}"


class CommentLike(models.Model):

    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "liked_by_comment")
    comment = models.ForeignKey(Comment, on_delete = models.CASCADE, related_name = "liked_comment")

    def __str__(self):
        return f"{self.user} Liked {self.comment}"


# class CommentComment(models.Model):
#     post = models.ForeignKey(Post, on_delete = models.CASCADE)

#     comment = models.ForeignKey(Comment, on_delete = models.CASCADE)

#     user = models.ForeignKey(User, on_delete = models.CASCADE)

#     content = models.CharField(max_length = 200)

#     time_stamp = models.DateTimeField(auto_now = False, auto_now_add = True)

#     likes = models.IntegerField(default = 0)

#     def __str__(self):
#         return f"By: {self.user}\nContent: {self.content}\nPosted: {self.time_stamp}\nLikes: {self.likes}\nOn Post: {self.post}"
