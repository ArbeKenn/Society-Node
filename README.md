# Society Node
The API for the Society Node social platform.
Posting, comments, feed, internal economy (coins),
and a perk and feature store.

## Stack
- FastAPI
- PostgreSQL
- SQLAlchemy (async)
- Alembic
- asyncpg
- PyJWT
- pwdlib (argon2)
- slowapi
- phonenumbers
- pydantic
- uvicorn
- python-dotenv

## Endpoints
- `GET /` - home

### Authentication
- `POST /user/reg` - registration
- `POST /user/log` - login
- `GET /user/my_profile` - profile 🔒
- `GET /user/my_profile/favorites` - my_favorites 🔒
- `GET /user/my_profile/my_items` - my_items 🔒
- `GET /user/my_profile/followers` - my_followers 🔒
- `GET /user/my_profile/following` - my_following 🔒
- `PUT /user/my_profile/edit` - edit_profile 🔒
- `DEL /user/my_profile/del` - del user 🔒
- `POST /follow/{target_user_id}` - followed and unfollowed 🔒
- `POST /followers/{user_id}` - another user followers and following

### Posts
- `GET /post/posts` - all posts
- `POST /post/new_post` - create post 🔒
- `GET /post/{post_id}` - detail post 🔒
- `PUT /post/edit` - edit post 🔒
- `DEL /post/del/{post_id}` - del post 🔒
- `POST /post/{post_id}/favorite` - added post in favorites 🔒
- `GET /posts/comment/{post_id}` - all comments in post 
- `POST /posts/comment/{post_id}` - create comment 🔒
- `PUT /posts/comment/{comment_id}` - edit comment 🔒
- `DEL /posts/comment/{comment_id}` - del comment 🔒
- `POST /posts/comment/{comment_id}/like` - like comment 🔒

### Shop
- `GET /shop/` - all items
- `POST /shop/{item_id}/by` - by item 🔒

### Notifications
- `GET /notifications/` - all comments 🔒

### Search
- `GET /search/post` - search posts
- `GET /search/user` - search users
- `GET /search/shop_item` - search items in shop

### Admin
- `GET /admin/` - admin 🔒🔒
- `POST /admin/item` - create new item_shop 🔒🔒
- `PUT /admin/item/{item_id}` - edit item 🔒🔒
- `DEL /admin/item/{item_id}` - del item 🔒🔒
- 
🔒 - requires a JWT token

🔒🔒 - Admin
 
---
 
# 🛠 Installation and Setup

### Requirements
To run via Docker, make sure you have installed [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/).

---

## Docker

### 1. Clone the repository
```bash
git clone [https://github.com/ArbeKenn/Society-Node.git](https://github.com/ArbeKenn/Society-Node.git)
cd Society-Node
```

### 2. Virtual environment
Create a .env file:
```bash
cp .env.example .env
```

### 3. Run containers:
```bash
docker compose up -d --build
```
To stop, use the command:
```bash
docker compose down
```

---

## Local (No Docker)
### 1. Clone the repository
```bash
git clone https://github.com/ArbeKenn/Society-Node.git
cd Society-Node
```
 
### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
```
 
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
 
### 4. Configure environment variables
Create a .env file:
```bash
cp .env.example .env
```

### 5. Initialize the database
```bash
# Create all tables
alembic upgrade head

# Create a new migration (after model changes)
alembic revision --autogenerate -m "your migration message"

# Apply migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1
```
### 6. Run the application
```bash
# Development mode
uvicorn app.main:app --reload

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```
 
## 🔗 API Documentation
Once the application is running, you can explore the API endpoints here:
Swagger UI: http://localhost:8000/docs
 
---
 
## 📁 Structure
 
```
Society Node/
├── app/
│   ├── admin/
│   │    ├── models.py
│   │    ├── schemas.py
│   │    └── router.py
│   ├── migrations/
│   │    ├── versions
│   │    └── env.py
│   ├── notifications/
│   │    ├── models.py
│   │    ├── schemas.py
│   │    └── router.py
│   ├── posts/
│   │    ├── routers/
│   │    │   ├── __init__.py
│   │    │   ├── comments.py
│   │    │   └── posts.py
│   │    ├── models.py
│   │    └── schemas.py
│   ├── search/
│   │    ├── schemas.py
│   │    └── router.py
│   ├── shop/
│   │    ├── models.py
│   │    ├── schemas.py
│   │    └── router.py
│   ├── user/
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── router.py
│   │   └── jwt.py
│   ├── __init__.py
│   ├── alembic.ini
│   ├── database.py
│   └── main.py
├── .env
├── .dockerignore
├── .gitignore
├── docker-compose.yml
├── Dockerfile
└── README.md
├── requirements.txt
```
---
 
## 👤 Author
 
Bektemir – [GitHub](https://github.com/ArbeKenn) – [Telegram](https://t.me/ArbeKenn) – [Email](mailto:bektemir1102@gmail.com)