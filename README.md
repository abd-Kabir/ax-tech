# Task from AX-TECHNOLOGY!
Я хотел поблагодарить что вы дали мне шанс, надеюсь я выполнил заданный таск правильно и получиться поработать с вами)

# Start Project

Install all packages from **requirements.txt** file
`pip install -r requirements.txt`

Create **.env** file, you can get example from **.env.example** file

Run migrations with alembic commands:
`alembic revision --autogenerate -m 'commit'`
`alembic upgrade head`

Run application with command:
`uvicorn src.main:app`

Link for [**OpenAPI/Swagger**](http://127.0.0.1:8000/docs)

PS: I did successfully run the project with docker-compose (app + db), but the alembic migrations would not work properly, so decided to not include docker version of the app.