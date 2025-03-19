import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from .models import *
from graphene.types import Interface
import graphql_jwt
from graphql import GraphQLError

from graphene_file_upload.scalars import Upload


User = get_user_model()

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email")

class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile
        fields = "__all__"

from django.core.files.storage import default_storage

class UploadProfilePicture(graphene.Mutation):
    class Arguments:
        profile_picture = Upload(required=True)

    success = graphene.Boolean()
    profile = graphene.Field(ProfileType)

    def mutate(self, info, profile_picture):
        user = info.context.user
        if not user.is_authenticated:
            raise GraphQLError("Authentication required!")

        profile, _ = Profile.objects.get_or_create(user=user)

        # Save file to media storage
        file_path = default_storage.save(f"profile_pics/{profile_picture.name}", profile_picture)
        profile.profile_picture = file_path
        profile.save()

        return UploadProfilePicture(success=True, profile=profile)





    
       

        
# Define an Interface for content types that can be commented on
class CommentContentInterface(Interface):
    id = graphene.ID()

# apply the Interface to PostType and StoryType
class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = "__all__"
        interfaces = (CommentContentInterface,)

class StoryType(DjangoObjectType):
    class Meta:
        model = Story
        fields = "__all__"
        interfaces = (CommentContentInterface,)

class CommentType(DjangoObjectType):
    content_object = graphene.Field(CommentContentInterface)

    class Meta:
        model = Comment
        fields = "__all__"

    def resolve_content_object(self, info):
        if isinstance(self.content_object, Post):
            return self.content_object
        if isinstance(self.content_object, Story):
            return self.content_object
        return None

class UploadPostImage(graphene.Mutation):
    class Arguments:
        image = Upload(required=True)
        caption = graphene.String(required=True)

    success = graphene.Boolean()
    post = graphene.Field(PostType)

    def mutate(self, info, image, caption):
        user = info.context.user
        if not user.is_authenticated:
            raise GraphQLError("Authentication required!")

        # Save file properly
        file_path = default_storage.save(f"post_images/{image.name}", image)

        post = Post.objects.create(
            created_by=user,
            image=file_path,
            caption=caption
        )
        return UploadPostImage(success=True, post=post)




class MessageType(DjangoObjectType):
    class Meta:
        model = Message
        fields = "__all__"

class NotificationType(DjangoObjectType):
    class Meta:
        model = Notification
        fields = "__all__"

class HashtagType(DjangoObjectType):
    class Meta:
        model = Hashtag
        fields = "__all__"

class PostSaveType(DjangoObjectType):
    class Meta:
        model = PostSave
        fields = "__all__"

class ReportType(DjangoObjectType):
    class Meta:
        model = Report
        fields = "__all__"

class CreatePost(graphene.Mutation):
    class Arguments:
        caption = graphene.String(required=True)
        image = Upload(required=True)  #  Fix: Use Upload for file handling
        created_by = graphene.ID(required=True)

    post = graphene.Field(PostType)

    def mutate(self, info, caption, image, created_by):
        user = User.objects.get(id=created_by)

        #  Save image properly
        file_path = default_storage.save(f"post_images/{image.name}", image)

        post = Post.objects.create(
            caption=caption,
            image=file_path,
            created_by=user,
            updated_by=user  # Fix: Assign same user to updated_by
        )

        return CreatePost(post=post)



class CreateComment(graphene.Mutation):
    class Arguments:
        text = graphene.String(required=True)
        post_id = graphene.ID(required=True)
        created_by = graphene.ID(required=True)
    
    comment = graphene.Field(CommentType)

    def mutate(self, info, text, post_id, created_by):
        user = User.objects.get(id=created_by)
        post = Post.objects.get(id=post_id)
        comment = Comment.objects.create(text=text, content_object=post, created_by=user)
        return CreateComment(comment=comment)

# Authentication Mutations
class ObtainToken(graphql_jwt.ObtainJSONWebToken):
    user = graphene.Field(UserType)

    def resolve_user(self, info, **kwargs):
        return info.context.user

class RefreshToken(graphql_jwt.Refresh):
    pass

class VerifyToken(graphql_jwt.Verify):
    pass

class RegisterUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, username, email, password):
        user = User.objects.create_user(username=username, email=email, password=password)
        return RegisterUser(user=user)

class PostLikeType(DjangoObjectType):
    class Meta:
        model = PostLike

class FollowType(DjangoObjectType):
    class Meta:
        model = Follow

class LikePost(graphene.Mutation):
    class Arguments:
        post_id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, post_id):
        user = info.context.user
        if not user.is_authenticated:
            raise GraphQLError("Authentication required!")

        post = Post.objects.get(id=post_id)

        # Check if user already liked
        like, created = PostLike.objects.get_or_create(user=user, post=post)

        if not created:
            like.delete()  # Unlike the post if already liked
            return LikePost(success=False)
        
        return LikePost(success=True)

class FollowUser(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, user_id):
        user = info.context.user
        if not user.is_authenticated:
            raise GraphQLError("Authentication required!")

        following = User.objects.get(id=user_id)
        if user == following:
            raise GraphQLError("You cannot follow yourself!")

        follow, created = Follow.objects.get_or_create(follower=user, following=following)

        if not created:
            follow.delete()  # Unfollow if already followed
            return FollowUser(success=False)

        return FollowUser(success=True)



class Mutation(graphene.ObjectType):
    
    register_user = RegisterUser.Field()
    token_auth = ObtainToken.Field()
    verify_token = VerifyToken.Field()
    refresh_token = RefreshToken.Field()
    create_post = CreatePost.Field()
    create_comment = CreateComment.Field()
    
    upload_profile_picture = UploadProfilePicture.Field()
    upload_post_image = UploadPostImage.Field()
    
    like_post = LikePost.Field()
    follow_user = FollowUser.Field()

class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    posts = graphene.List(PostType)
    comments = graphene.List(CommentType)
    stories = graphene.List(StoryType)
    messages = graphene.List(MessageType)
    notifications = graphene.List(NotificationType)
    hashtags = graphene.List(HashtagType)
    post_saves = graphene.List(PostSaveType)
    reports = graphene.List(ReportType)
    
    def resolve_users(self, info):
        user = info.context.user
        if not user.is_authenticated:
            raise GraphQLError("Authentication required!")

        return User.objects.all()

    
    def resolve_posts(self, info):
        user = info.context.user
        if not user.is_authenticated:
            raise GraphQLError("Authentication required!")

        return Post.objects.filter(created_by=user)  # ✅ Only return the user's posts

    
    def resolve_comments(self, info):
        user = info.context.user
        if not user.is_authenticated:
            raise GraphQLError("Authentication required!")

        return Comment.objects.filter(content_object__created_by=user)  # ✅ Filter by user

    
    def resolve_stories(self, info):
        return Story.objects.all()
    
    def resolve_messages(self, info):
        return Message.objects.all()
    
    def resolve_notifications(self, info):
        return Notification.objects.all()
    
    def resolve_hashtags(self, info):
        return Hashtag.objects.all()
    
    def resolve_post_saves(self, info):
        return PostSave.objects.all()
    
    def resolve_reports(self, info):
        return Report.objects.all()

schema = graphene.Schema(query=Query, mutation=Mutation)
