
# JWT Token Authentication Demo

This is a simple demonstration of how to implement JWT Token Authentication in a Django project using the `djangorestframework` and `djangorestframework-simplejwt` packages.

## Overview

JWT (JSON Web Token) is an open standard for securely transmitting information between parties as a JSON object. It is commonly used in web applications for authentication, and it provides a stateless mechanism to verify the user's identity without requiring the server to store any session information.

JWT tokens consist of three parts:
1. **Header**: Specifies the signing algorithm and type of token (JWT).
2. **Payload**: Contains the claims (user data or any other information).
3. **Signature**: A cryptographic signature used to verify that the sender of the JWT is who it says it is and that the message wasn't changed along the way.

In this demo, we will demonstrate how to use JWT to authenticate users in Django, allowing you to interact with an API securely.

## Setup

### 1. Install Required Packages

To get started, install the following packages:

```bash
pip install djangorestframework
pip install djangorestframework-simplejwt
```

### 2. Django Settings Configuration

In the `settings.py` file, make the following changes:

```python
INSTALLED_APPS = [
    'rest_framework',  # Add Django Rest Framework
    'rest_framework.authtoken',  # Optional if you're also using the DRF token auth
]

# REST Framework settings for JWT Authentication
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # Requires authentication
    ],
}

# Optional Simple JWT settings to configure the expiration time of the tokens
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),  # Set the token expiration time (15 minutes)
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),  # Set refresh token expiration time (1 day)
    'ROTATE_REFRESH_TOKENS': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': 'your-secret-key',  # Secret key for encoding/decoding JWT tokens
}
```

### 3. URL Configuration

Update the `urls.py` file to include endpoints for obtaining and refreshing tokens, and for accessing protected resources:

```python
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),  # Include URLs from your app
    # Token obtain pair (used to get access and refresh tokens)
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),  
    # Token refresh (used to refresh the JWT token when it expires)
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
```

### 4. Views and Authentication

In your `views.py`, create views that require authentication using JWT tokens:

```python
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Create a class-based view that requires JWT authentication
class HelloView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        content = {'message': 'Hello, this is a message from the API'}
        return Response(content)

# Simple function-based view to render the homepage
def index(request):
    return render(request, 'index.html')
```

### 5. Running the Server

Run the Django development server:

```bash
python manage.py runserver
```

Your application will be available at `http://127.0.0.1:8000/`.

### 6. Testing with Postman

- **Step 1:** Obtain a JWT Token
  - Make a POST request to `http://127.0.0.1:8000/api/token/` with the following body parameters:
    ```bash
    username=your_username
    password=your_password
    ```
  - You will receive a response with an `access` token and a `refresh` token:
    ```json
    {
        "access": "YOUR_ACCESS_TOKEN",
        "refresh": "YOUR_REFRESH_TOKEN"
    }
    ```

- **Step 2:** Use the Token for Authentication
  - In Postman, send a GET request to `http://127.0.0.1:8000/hello/` with the following headers:
    ```bash
    Authorization: Bearer YOUR_ACCESS_TOKEN
    ```

- **Step 3:** Token Refresh (Optional)
  - If the access token has expired, you can refresh it by sending a POST request to `http://127.0.0.1:8000/api/token/refresh/` with the `refresh` token you received earlier:
    ```json
    {
        "refresh": "YOUR_REFRESH_TOKEN"
    }
    ```

## Explanation of JWT Flow

1. **Obtain Token**:
   - The user submits their credentials (username and password) to the `/api/token/` endpoint.
   - If the credentials are valid, the server responds with a JWT containing an `access` token and a `refresh` token.

2. **Access API Endpoints**:
   - To access protected resources, the client must include the `access` token in the `Authorization` header:
     ```bash
     Authorization: Bearer YOUR_ACCESS_TOKEN
     ```

3. **Token Expiry & Refresh**:
   - JWT tokens typically have an expiration time (`ACCESS_TOKEN_LIFETIME`).
   - When the token expires, the client can use the `refresh` token to obtain a new `access` token by making a request to the `/api/token/refresh/` endpoint.

## Security Notes

- Keep the **secret key** safe, as it is used to sign the JWT tokens.
- Treat JWT tokens like passwords and never expose them in public repositories.
- Ensure your application uses HTTPS to prevent token interception via man-in-the-middle attacks.

## Conclusion

This demo implements JWT Token Authentication using Django and DRF, allowing you to secure your API and manage access based on authenticated tokens. By utilizing the `djangorestframework-simplejwt` package, we have created endpoints for obtaining and refreshing tokens, along with views that require authentication to access protected data.
