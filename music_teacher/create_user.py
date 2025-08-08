from music_teacher import app, db
from music_teacher.models import User
from werkzeug.security import generate_password_hash

with app.app_context():
    username = input("Введите логин нового пользователя: ")
    password = input("Введите пароль: ")

    # Проверка, существует ли уже такой пользователь
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        print("Пользователь с таким логином уже существует.")
    else:
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        print(f"Пользователь '{username}' успешно создан.")
