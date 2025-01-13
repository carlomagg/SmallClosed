# API Endpoints Documentation

## Base URL
All endpoints are prefixed with: `http://localhost:8000/api/users/`

## Authentication
- Most endpoints require JWT authentication
- Include the token in the Authorization header: `Authorization: Bearer <access_token>`

## Endpoints

### 1. User Registration
**Endpoint:** `POST /register/`
**Access:** Public
**Description:** Register a new user account

**Request Body:**
json
{
"email": "user@example.com",
"username": "username",
"password": "strong_password",
"password2": "strong_password"
}

**Response:**


json
{
"message": "User registered successfully. Please check your email for verification.",
"user": {
"email": "user@example.com",
"username": "username"
},
"tokens": {
"refresh": "<refresh_token>",
"access": "<access_token>"
}
}


### 2. Email Verification
**Endpoint:** `GET /verify-email/<token>/`
**Access:** Public
**Description:** Verify user's email address using the token sent to their email

**Response:**

json
{
"message": "Email verified successfully"
}


### 3. User Login
**Endpoint:** `POST /login/`
**Access:** Public
**Description:** Authenticate user and receive JWT tokens

**Request Body:**
json
{
"email": "user@example.com",
"password": "your_password"
}

**Response:**

json
{
"refresh": "<refresh_token>",
"access": "<access_token>"
}

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify_email'),
]
