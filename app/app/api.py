from ninja import NinjaAPI, Schema, UploadedFile, File
from django.contrib.auth.models import User
from django.contrib.auth import (
    get_user_model,
    authenticate
)

api = NinjaAPI()

class HelloSchema(Schema):
    name: str = "World"


class UserIn(Schema):
    email: str
    username: str
    password: str


class UserOut(Schema):
    id: int
    email: str
    username: str
    firstname: str = None
    surname: str = None
    role: str = None
    avatar: str = None


class Error(Schema):
    message: str


@api.api_operation(["GET", "POST"], "/users/", response={200: UserOut, 400: Error, 403: Error})
def manage_users(request, data: UserIn):
    """Manage user profiles."""
    if request.get:
        if not request.user.is_authenticated:
            return 403, {"message": "Please sign in first"}
        return request.user 
    elif request.post: 
        try: 
            username = data.username
            email = data.email
            password = data.password
            user = get_user_model().objects.create_user(
                username=username,
                email=email,
                password=password
            )
            return user
        except:
            return 400, {"message": "Incorrect syntax or an invalid request structure. Please try again."}
