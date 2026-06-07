# Society Node
The API for the Society Node social platform. Posting, comments, feed, internal economy (coins), and a perk and feature store

## Steak
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
-
- `POST /user/reg` - registration
- `POST /user/log` - login
- `GET /user/my_profile` - profile 🔒
- `GET /user/my_profile/favorites` - my_favorites 🔒
- `GET /user/my_profile/followers` - my_followers 🔒
- `GET /user/my_profile/following` - my_following 🔒
- `PUT /user/my_profile/edit` - edit_profile 🔒
- `DEL /user/my_profile/del` - del user 🔒
- `POST /follow/{target_user_id}` - followed and unfollowed 🔒
- `POST /followers/{user_id}` - another user followers and following


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

🔒 — requires a JWT token
 
---
 
## 🛠 Установка и запуск
 
### 1. Клонировать репозиторий
```
git clone https://github.com/ArbeKenn/Society-Node.git
cd Hive
```
 
### 2. Создать виртуальное окружение
```
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
```
 
### 3. Установить зависимости
```
pip install -r requirements.txt
```
 
### 4. Настроить переменные окружения
 
Создай файл `.env` в корне проекта:
```
DATABASE_URL=your_database
SECRET_KEY=your_secret_key
```
 
### 5. Запустить приложение
```
uvicorn app.main:app --reload
```
 
После запуска открой в браузере:  
Swagger UI: http://localhost:8000/docs
 
---
 
## 📁 Structure
 
```
Society Node/
├── app/
│   ├── migrations/
│   │    ├── versions
│   │    └── env.py
│   ├── posts/
│   │    ├── posts/
│   │    │   ├── __init__.py
│   │    │   ├── comments.py
│   │    │   └── posts.py
│   │    ├── models.py     
│   │    └── schemas.py      
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
├── .gitignore
├── requirements.txt
└── README.md
```
---
 
## 👤 Author
 
Bektemir – [GitHub](https://github.com/ArbeKenn) – [Telegram](https://t.me/ArbeKenn) – [Email](mailto:bektemir1102@gmail.com)