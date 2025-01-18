Implementing Token Authentication Using REST


## Token Authentication

This demo uses **Token Authentication** to secure the API. The `Token` header is used to authenticate users via the following steps:

### 1. Obtain a Token

To obtain a token, you can either use the `/api-token-auth/` endpoint or manually create a token for a user in the Django admin.

**POST** request to the `/api-token-auth/` endpoint:

- **URL**: `http://127.0.0.1:8000/api-token-auth/`
- **Body** (Form Data):
  - `username`: your_username
  - `password`: your_password

On success, you'll receive a response like this:

```json
{
    "token": "YOUR_TOKEN_HERE"
}
```

Save the token for use in subsequent API requests.

### 2. Use the Token for Authentication

Once you have the token, include it in the `Authorization` header of your API requests.

#### Example:
**GET** request to list users (replace `YOUR_TOKEN_HERE` with the actual token):

```bash
http http://127.0.0.1:8000/api/app/ "Authorization: Token YOUR_TOKEN_HERE"
```

**POST** request to create a new user:

```bash
http POST http://127.0.0.1:8000/api/app/ "Authorization: Token YOUR_TOKEN_HERE" username="newuser" password="password" email="newuser@example.com"
```

### 3. API Endpoints

Here are the available endpoints:

#### `/api/app/`
- **GET**: List all users.
- **POST**: Create a new user (requires token).
- **PUT/PATCH**: Update an existing user (requires token).
- **DELETE**: Delete an existing user (requires token).

#### `/api-token-auth/`
- **POST**: Authenticate a user and get a token. This endpoint requires a username and password.

## Token Authentication Used

This demo uses **DRF's Token Authentication** system, which is a simple and efficient way to secure API endpoints by requiring a token with each request. The token is generated using the DRF `rest_framework.authtoken` package.

The flow involves:
1. A client sends a username and password to the `/api-token-auth/` endpoint.
2. The server returns a token if the credentials are correct.
3. The client sends the token in the `Authorization` header with subsequent API requests.