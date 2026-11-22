# APIlearn — Authentication & Todo REST API

A full-stack learning project built with **FastAPI** that combines user authentication, token-based authorization, database-backed Todo management, and a frontend interface.

The project explores how a backend application handles user registration, login, authentication, protected routes, database operations, and communication between a frontend and backend.

## Features

- **User registration** — Create accounts with username and password.
- **User authentication** — Authenticate users using username and password.
- **JWT authentication** — Generate access tokens for authenticated users.
- **Password hashing** — Hash passwords before storing them in the database.
- **Protected endpoints** — Restrict access to routes requiring authentication.
- **User profile endpoint** — Retrieve information about the currently authenticated user.
- **Todo management** — Create and retrieve Todo items.
- **User-specific data** — Associate Todo records with individual users.
- **Database integration** — Persist users and Todo records using SQLAlchemy.
- **Frontend integration** — Includes a frontend directory for the Todo interface.
- **Request logging** — Log incoming HTTP requests and outgoing responses.
- **CORS configuration** — Configure cross-origin requests for frontend integration.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core backend language |
| FastAPI | API framework |
| SQLAlchemy | ORM and database operations |
| SQLite / configured database | Data persistence |
| Pydantic | Request validation and response schemas |
| JWT | Authentication tokens |
| Passlib + bcrypt | Password hashing |
| OAuth2 | Authentication flow |
| Uvicorn | ASGI server |
| HTML / CSS / JavaScript | Frontend (depending on implementation) |

## Architecture

```mermaid
flowchart TD
    A[Frontend Client] --> B[FastAPI Application]
    B --> C[Routes and Request Validation]
    C --> D[Authentication and Authorization]
    C --> E[CRUD Operations]
    D --> F[JWT Token Verification]
    E --> G[SQLAlchemy]
    G --> H[(Database)]
    H --> G
    G --> E
    E --> C
    C --> B
    B --> A
```

## Project Structure

```text
apilearn/
│
├── main.py          # FastAPI application and routes
├── auth.py         # Authentication, JWT and DB dependencies
├── crud.py         # Database operations
├── database.py     # Database connection and session setup
├── models.py       # SQLAlchemy database models
├── schemas.py      # Pydantic schemas
├── init_db.py     # Database initialization
├── requirements.txt
│
├── todo-frontend/  # Frontend application
│
├── .env           # Environment configuration
└── README.md
```

## API Endpoints

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| `GET` | `/` | Health check | No |
| `POST` | `/signup` | Register a new user | No |
| `POST` | `/token` | Login and obtain access token | No |
| `GET` | `/users/me` | Get current authenticated user | Yes |
| `POST` | `/todos` | Create a Todo | Yes |
| `GET` | `/todos` | Retrieve current user's Todos | Yes |

## Authentication Flow

The application uses a token-based authentication system.

```mermaid
sequenceDiagram
    participant U as User / Frontend
    participant A as FastAPI
    participant D as Database

    U->>A: POST /signup
    A->>D: Create user with hashed password
    D-->>A: User record
    A-->>U: Registration response

    U->>A: POST /token (credentials)
    A->>D: Retrieve user
    D-->>A: User and password hash
    A->>A: Verify password
    A->>A: Generate JWT
    A-->>U: Access token

    U->>A: Request protected endpoint + Bearer token
    A->>A: Validate JWT
    A->>D: Retrieve authenticated user
    D-->>A: User data
    A-->>U: Protected resource
```

### Authentication Components

- **Password hashing:** Passwords are hashed before storage using bcrypt.
- **Login:** Credentials are verified against the stored password hash.
- **Access token:** A JWT is generated after successful authentication.
- **Token expiration:** Access tokens have a configurable expiration duration.
- **Protected routes:** Authentication dependencies validate the token and resolve the current user.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/sikker357/apilearn.git
```

### 2. Navigate to the project directory

```bash
cd apilearn
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

Activate the environment:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root.

```env
SECRET_KEY=replace_with_a_secure_random_secret
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

The application loads configuration using `python-dotenv`.

> Do not commit real secret keys or credentials to GitHub.

## Running the Application

Run the FastAPI application from the appropriate package context using Uvicorn.

```bash
uvicorn main:app --reload
```

If the project is structured or imported as a Python package, use the appropriate module path for your setup.

Default development address:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI automatically generates interactive API documentation.

| Documentation | URL |
|---|---|
| Swagger UI | `http://127.0.0.1:8000/docs` |
| ReDoc | `http://127.0.0.1:8000/redoc` |

Use the Swagger UI to explore routes, submit requests, register accounts, authenticate, and test protected endpoints.

## API Usage

### 1. Register a user

**Endpoint**

```http
POST /signup
```

**Request body**

```json
{
  "username": "alex",
  "password": "your_password"
}
```

Creates a new account and returns the user information according to the response schema.

### 2. Login

**Endpoint**

```http
POST /token
```

The login endpoint uses OAuth2 form-based credentials.

**Form fields**

```text
username: alex
password: your_password
```

**Example response**

```json
{
  "access_token": "your_jwt_access_token",
  "token_type": "bearer"
}
```

### 3. Get the current user

**Endpoint**

```http
GET /users/me
```

**Authorization header**

```http
Authorization: Bearer your_jwt_access_token
```

Returns the authenticated user's information.

### 4. Create a Todo

**Endpoint**

```http
POST /todos
```

Requires a valid access token.

Submit the Todo data according to the `TodoCreate` schema defined in `schemas.py`.

### 5. Retrieve Todos

**Endpoint**

```http
GET /todos
```

Returns Todo records belonging to the currently authenticated user.

## Database Design

The application uses SQLAlchemy models to represent database records.

The primary entities include:

- **User** — Stores account information and password hashes.
- **Todo** — Stores Todo records associated with a user.

The relationship between users and Todo records allows each authenticated user to retrieve their own data.

```mermaid
erDiagram
    USER ||--o{ TODO : owns
    USER {
        integer id
        string username
        string hashed_password
    }
    TODO {
        integer id
        string title
        boolean completed
        integer user_id
    }
```

*Conceptual relationship diagram.*

## Core Modules

| File | Responsibility |
|---|---|
| `main.py` | Application initialization, routes, middleware and request handling |
| `auth.py` | Password hashing, JWT creation and validation, database dependency and current-user resolution |
| `crud.py` | Database read/write operations |
| `database.py` | Engine, session configuration and database connection |
| `models.py` | SQLAlchemy models |
| `schemas.py` | Request/response validation schemas |
| `init_db.py` | Database initialization |
| `todo-frontend/` | Frontend interface |

## Security Considerations

- Passwords are hashed rather than stored in plaintext.
- JWT authentication is used to protect endpoints.
- Protected routes resolve the identity of the authenticated user.
- Access token expiration is configurable.
- Secret keys should be loaded from environment variables.
- Debug and development configurations should not be used in production.
- The application should use a strong, unique secret key.

## Limitations & Future Improvements

- Add complete CRUD operations for Todo items, including update and delete.
- Improve request validation and error responses.
- Implement refresh tokens and token revocation.
- Add email verification and password reset functionality.
- Improve frontend authentication and token management.
- Add automated testing using Pytest.
- Add migrations using Alembic.
- Add structured logging.
- Improve deployment configuration.
- Containerize the application using Docker.
- Add rate limiting and additional security controls.

## Learning Objectives

This project explores:

- FastAPI application development
- REST API design
- User registration and login
- Password hashing
- JWT authentication
- OAuth2 password flow
- Dependency injection
- Protected routes
- SQLAlchemy ORM
- Database sessions and relationships
- Pydantic schemas and validation
- Frontend–backend integration
- CORS
- HTTP status codes
- Modular backend architecture

---

**APIlearn — a hands-on project exploring authentication, database-backed APIs, and backend application architecture with FastAPI.**
