# FastAPI — Core Concepts & Learning Project

A hands-on project built while learning the **core concepts of FastAPI**, a modern, high-performance Python web framework.

---

## What I Learned

### 1. FastAPI App Setup
- Creating a FastAPI instance with `FastAPI()`
- Running the app using **Uvicorn** as the ASGI server

### 2. Path Operations (Routes)
- Defining routes using decorators: `@app.get()`, `@app.post()`, `@app.put()`, `@app.delete()`
- Understanding **HTTP methods** and when to use each

### 3. Request Body & Pydantic Models
- Using `pydantic.BaseModel` to define and validate request body schemas
- Parsing incoming JSON data automatically into typed Python models

### 4. Path Parameters & Type Validation
- Extracting dynamic values from URLs using `{id}` syntax
- FastAPI automatically validates and converts types (e.g., `id: int`)

### 5. Response & Status Codes
- Returning custom HTTP status codes using `status` from `fastapi`
- Using the `Response` object to set status codes dynamically
- Setting default status codes directly on route decorators (e.g., `status_code=204`)

### 6. HTTPException & Error Handling
- Raising `HTTPException` with proper status codes and detail messages
- Handling **404 Not Found** when a resource doesn't exist

### 7. In-Memory Data Store (CRUD)
- Simulating a database using a Python list (`my_posts`)
- Implementing full **CRUD** operations:
  - **Create** — `POST /posts`
  - **Read All** — `GET /posts`
  - **Read One** — `GET /posts/{id}`
  - **Update** — `PUT /posts/{id}`
  - **Delete** — `DELETE /posts/{id}`

---

## API Endpoints

| Method | Endpoint       | Description              |
|--------|----------------|--------------------------|
| GET    | `/`            | Welcome message          |
| POST   | `/login`       | User login               |
| GET    | `/posts`       | Get all posts            |
| POST   | `/posts`       | Create a new post        |
| GET    | `/posts/{id}`  | Get a single post by ID  |
| PUT    | `/posts/{id}`  | Update a post by ID      |
| DELETE | `/posts/{id}`  | Delete a post by ID      |

---

## Project Structure

```
FASTAPI/
├── app/
│   ├── __init__.py
│   └── main.py
├── .gitignore
└── README.md
```

---

## How to Run

```bash
# Install dependencies
pip install fastapi uvicorn

# Start the server
uvicorn app.main:app --reload
```

Then open your browser at `http://127.0.0.1:8000/docs` to explore the **interactive Swagger UI**.

---

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/)
- [Uvicorn](https://www.uvicorn.org/)
