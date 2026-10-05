uvicorn app.main:app --reload


blog-management-api/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
├── auth.py
│
├── routers/
│   ├── auth.py
│   └── posts.py
│
├── media/
│   └── posts/
│
├── blog.db
└── requirements.txt