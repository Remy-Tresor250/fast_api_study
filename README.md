# FastAPI User Authentication and Visit Request API

This project is a RESTful API built with **FastAPI**, enabling user authentication and management, as well as visit request handling. It includes features like user registration, login, and secure token-based authentication.

## Features

- **User Authentication**: Implemented user auth using JWT.
- **User Management**: Create and retrieve user details.
- **Visit Requests**: Handle visit requests with organization details and status tracking.

## Tech Stack

- **FastAPI**: Python web framework for building APIs.
- **SQLAlchemy**: ORM for database management.
- **JWT (JSON Web Tokens)**: For secure user authentication.
- **Pydantic**: Data validation and serialization.
- **SQLite**: Default database for development.

## Setup Instructions

### Prerequisites

- Python 3.9 or higher installed on your system.
- A virtual environment setup (optional but recommended).

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Remy-Tresor250/fast_api_study.git
   cd fast_api_study
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database:

   ```bash
   python -m app.main
   ```

### Running the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

### API Endpoints

#### User Endpoints

- **Register a User**:
  - **POST** `/users/`
  - **Request Body**:

    ```json
    {
      "username": "trex",
      "email": "trex@example.com",
      "password": "trex1234",
      "role": "user"
    }
    ```

- **Login**:
  - **POST** `/token`
  - **Form Data**:

    ```json
    {
      "username": "trex",
      "password": "trex1234"
    }
    ```

  - **Response**:

    ```json
    {
      "access_token": "<JWT_TOKEN>",
      "token_type": "bearer"
    }
    ```

#### Visit Request Endpoints

- **Create a Visit Request**:
  - **POST** `/visit-requests/`
  - **Request Body**:

    ```json
    {
      "organization_name": "Tech Corp",
      "visit_date": "2024-12-01T00:00:00",
      "visit_start_time": "2024-12-01T10:00:00",
      "visit_end_time": "2024-12-01T12:00:00"
    }
    ```

- **Get All Visit Requests**:
  - **GET** `/visit-requests/`

### Database Models

- **User**:
  - `id`, `username`, `email`, `password`, `role`
- **VisitRequest**:
  - `id`, `organization_name`, `visit_date`, `visit_start_time`, `visit_end_time`, `status`

### Security

- Passwords are hashed using **bcrypt**.
- Tokens are signed with a secret key using **HS256** algorithm.

### Contact

For questions or collaboration, contact:

- **Name**: Remy Tresor
- **Email**: niyitegekatresor@gmail.com
- **GitHub**: [GitHub Profile](https://github.com/Remy-Tresor250)
