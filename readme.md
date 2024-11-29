# Setup

## Install docker desktop
- [Docker Desktop](https://www.docker.com/products/docker-desktop)

```bash
git clone 
cd into the project
docker-compose up
```

## API Endpoints

Register a New User
Endpoint: POST /register
Description: Registers a new user in the system.

Example Request:
```bash
curl -X POST http://localhost:5000/register \
-H "Content-Type: application/json" \
-d '{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "username": "johndoe",
  "password": "securepassword"
}'
```
Example Successful Response
```json
{
  "message": "User registered successfully"
}
```

Error Responses
- 400 Bad Request: {"error": "All fields are required"}
- 400 Bad Request: {"error": "Username already exists"}
- 400 Bad Request: {"error": "Email already exists"}


Login an Existing User
Endpoint: POST /login
Description: Logs in an existing user with their username and password.

Example Request
```bash
curl -X POST http://localhost:5000/login \
-H "Content-Type: application/json" \
-d '{
  "username": "johndoe",
  "password": "securepassword"
}'
```

Example Successful Response
```json
{
  "message": "Login successful
}
```

