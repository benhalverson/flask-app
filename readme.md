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
  "message": "User registered successfully",
  "token": "<your_jwt_token>"
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
  "message": "Welcome, John Doe!",
  "token": "<your_jwt_token>"
}

```

Authenticated Endpoints
The following endpoints require a valid JWT token in the Authorization header.
Header Format:
```bash
Authorization: Bearer <your_jwt_token>
```


Get All Members
Endpoint: GET /members
Description: Retrieves a list of all members.

Example Request

```bash
curl -X GET http://localhost:5000/members \
-H "Authorization Bearer <your_jwt_token>"
```

Update Member
Endpoint: PUT /update/<member_id>
Description: Updates a member's data.

Example Request

```bash
curl -X PUT http://localhost:5000/update/1 \
-H "Authorization: Bearer <your_jwt_token>" \
-H "Content-Type: application/json" \
-d '{
  "name": "Updated Name",
  "email": "updated.email@example.com"
}'
```

Example Successful Response
```json
{
  "message": "Member updated successfully"
}

```

Delete Member
Endpoint: DELETE /delete/<member_id>
Description: Deletes a member by their ID.

Example Request
```bash
curl -X DELETE http://localhost:5000/delete/1 \
-H "Authorization: Bearer <your_jwt_token>"
```

Example Successful Response
```json
{
  "message": "Member deleted successfully"
}

```