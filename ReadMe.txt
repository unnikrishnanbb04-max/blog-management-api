blog-management-api/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
├── auth.py
├── settings.py              
├── .env                     
├── .gitignore               
│
├── routers/
│   ├── auth.py
│   └── posts.py
│
├── services/                
│   ├── __init__.py
│   ├── email_service.py
│   └── notification_service.py
│
├── media/
│   └── posts/
│
├── blog.db
└── requirements.txt



pip install pydantic-settings


uvicorn app.main:app --reload






