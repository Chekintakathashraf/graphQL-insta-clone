from django.contrib.auth import get_user_model
from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="%(class)s_created", on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, related_name="%(class)s_updated", on_delete=models.CASCADE)

    class Meta:
        abstract = True




# User Profile (OneToOne with User)
class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to="profile_pics/", blank=True)
    followers = models.ManyToManyField("self", symmetrical=False, related_name="following")

    def __str__(self):
        return self.user.username


# Post Model
class Post(BaseModel):
    caption = models.TextField()
    image = models.ImageField(upload_to="posts/")
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)

    def __str__(self):
        return f"Post by {self.created_by.username}"


# Comment Model (Using GenericForeignKey)
class Comment(BaseModel):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    text = models.TextField()
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies")

    def __str__(self):
        return f"Comment by {self.created_by.username}"


# Story Model
class Story(BaseModel):
    image = models.ImageField(upload_to="stories/")
    viewers = models.ManyToManyField(User, related_name="viewed_stories", blank=True)

    def __str__(self):
        return f"Story by {self.created_by.username}"


# Message Model (For Direct Messages)
class Message(BaseModel):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    text = models.TextField()
    seen = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"


# Notification Model
class Notification(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    text = models.TextField()
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}"


# Hashtag Model
class Hashtag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    posts = models.ManyToManyField(Post, related_name="hashtags")

    def __str__(self):
        return f"#{self.name}"


# Post Save (For saved posts/bookmarks)
class PostSave(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} saved a post"


# Report Model
class Report(BaseModel):
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    reason = models.TextField()

    def __str__(self):
        return f"Report by {self.reported_by.username}"
