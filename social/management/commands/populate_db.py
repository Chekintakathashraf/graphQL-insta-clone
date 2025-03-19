import random
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from faker import Faker
from social.models import Profile, Post, Comment, Story, Message, Notification, Hashtag, PostSave, Report

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = "Populate the database with dummy data"

    def handle(self, *args, **kwargs):
        self.create_users(10)
        self.create_profiles()
        self.create_posts(20)
        self.create_comments(30)
        self.create_stories(15)
        self.create_messages(25)
        self.create_notifications(20)
        self.create_hashtags(10)
        self.create_post_saves(10)
        self.create_reports(5)
        
        self.stdout.write(self.style.SUCCESS("Successfully populated the database!"))

    def create_users(self, count):
        for _ in range(count):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password="password123"
            )
            self.stdout.write(f"Created user: {user.username}")
    
    def create_profiles(self):
        for user in User.objects.all():
            Profile.objects.create(
                user=user,
                bio=fake.sentence(),
                profile_pic=fake.image_url(),
                created_by=user,  # Assign user to created_by
                updated_by=user
            )
            self.stdout.write(f"Created profile for: {user.username}")
    
    def create_posts(self, count):
        users = list(User.objects.all())
        for _ in range(count):
            post = Post.objects.create(
                caption=fake.text(),
                image=fake.image_url(),
                created_by=random.choice(users),
                updated_by=random.choice(users)
            )
            self.stdout.write(f"Created post: {post.caption}")
    
    def create_comments(self, count):
        users = list(User.objects.all())
        posts = list(Post.objects.all())
        for _ in range(count):
            comment = Comment.objects.create(
                text=fake.sentence(),
                content_object=random.choice(posts),
                created_by=random.choice(users),
                updated_by=random.choice(users)
            )
            self.stdout.write(f"Created comment: {comment.text}")
    
    def create_stories(self, count):
        users = list(User.objects.all())
        for _ in range(count):
            story = Story.objects.create(
                image=fake.image_url(),
                created_by=random.choice(users),
                updated_by=random.choice(users)
            )
            self.stdout.write(f"Created story for: {story.created_by.username}")
    
    def create_messages(self, count):
        users = list(User.objects.all())
        for _ in range(count):
            sender, receiver = random.sample(users, 2)
            message = Message.objects.create(
                sender=sender,
                receiver=receiver,
                text=fake.sentence(),
                created_by=sender,
                updated_by=sender
            )
            self.stdout.write(f"Message from {sender.username} to {receiver.username}")
    
    def create_notifications(self, count):
        users = list(User.objects.all())
        for _ in range(count):
            notification = Notification.objects.create(
                user=random.choice(users),
                text=fake.sentence(),
                created_by=random.choice(users),
                updated_by=random.choice(users)
            )
            self.stdout.write(f"Created notification: {notification.text}")
    
    def create_hashtags(self, count):
        for _ in range(count):
            hashtag, created = Hashtag.objects.get_or_create(name=fake.word())
            self.stdout.write(f"Created hashtag: {hashtag.name}")
    
    def create_post_saves(self, count):
        users = list(User.objects.all())
        posts = list(Post.objects.all())
        for _ in range(count):
            post_save = PostSave.objects.create(
                user=random.choice(users),
                post=random.choice(posts),
                created_by=random.choice(users),
                updated_by=random.choice(users)
            )
            self.stdout.write(f"Post saved by {post_save.user.username}")
    
    def create_reports(self, count):
        users = list(User.objects.all())
        posts = list(Post.objects.all())
        for _ in range(count):
            report = Report.objects.create(
                reported_by=random.choice(users),
                content_object=random.choice(posts),
                reason=fake.sentence(),
                created_by=random.choice(users),
                updated_by=random.choice(users)
            )
            self.stdout.write(f"Created report: {report.reason}")
