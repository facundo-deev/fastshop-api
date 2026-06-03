# FastShop API

## What is this project?
A REST API that replicates the core functionality of an e-commerce platform.
Built as a learning project, with plans to add more features over time.

## Technologies used
- **Python** — main language
- **FastAPI** — web framework for building the API
- **PostgreSQL** — relational database
- **psycopg2** — library to connect Python with PostgreSQL
- **Pydantic** — data validation
- **python-dotenv** — environment variables management

## How to install and run

### 1. Clone the repository
git clone https://github.com/facundo-deev/fastshop.git

### 2. Install dependencies
pip install fastapi uvicorn psycopg2-binary python-dotenv

### 3. Create a .env file
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database
DB_USER=postgres
DB_PASSWORD=your_password

### 4. Run the server
uvicorn main:app --reload

### 5. Open the docs
http://127.0.0.1:8000/docs