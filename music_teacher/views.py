from flask import request, redirect, url_for, render_template, flash, get_flashed_messages
from flask_mail import Message
from flask_login import login_user, logout_user, login_required

from . import app, mail
from .models import LearningProcess, LessonPrice, TextData, User

@app.route('/')
def index():
    prices = LessonPrice.query.all()
    textdata = TextData.query.all()
    learningitems = LearningProcess.query.all()
    return render_template('index.html', prices=prices, textdata = textdata, learningitems = learningitems)


@app.route('/callback', methods=['GET', 'POST'])
def callback():
    print("callback invoked")
    prices = LessonPrice.query.all()
    textdata = TextData.query.all()
    learningitems = LearningProcess.query.all()
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        message_text = request.form.get('message')

        try:
            print("Trying to send email")
            msg = Message(
                subject='Новый запрос на звонок',
                sender=app.config['MAIL_USERNAME'],
                recipients=[app.config['RECIPIENT_MAIL_USERNAME']]
            )
            msg.body = f"Имя: {name}\nТелефон: {phone}\nКомментарий: {message_text}"

            mail.send(msg)
            print("Email sent")

            flash('Спасибо! Ваша заявка отправлена.', 'success')

        except Exception as e:
            print(e)
            flash('Произошла ошибка при отправке. Попробуйте позже.', 'error')

        
        messages = get_flashed_messages()
        if messages:
            for message in messages:
                print(message)

        print("Redirecting")
        return redirect(url_for('index'))

    print("Rendering page")
    return render_template('index.html', prices=prices, textdata = textdata, learningitems = learningitems)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(request.args.get('next') or url_for('admin.index'))
        else:
            return "Неверные данные", 401
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
