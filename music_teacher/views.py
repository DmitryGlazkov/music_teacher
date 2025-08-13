from datetime import time
from flask import (flash, redirect, render_template,
                   request, url_for)
from flask_login import login_required, login_user, logout_user
from flask_mail import Message

from . import app, mail
from .models import LearningProcess, LessonPrice, TextData, User


def get_lesson_info(id_):
    lesson = LessonPrice.query.get(id_)
    if not lesson:
        return {}
    return {
        'lesson_name': lesson.lesson_name,
        'price_duration': lesson.price_duration,
        'comment': lesson.comment
    }


def get_prices():
    return {
        'free_trial_lesson': get_lesson_info(1),
        'group_lesson': get_lesson_info(2),
        'individual_lesson': get_lesson_info(3),
        'individual_lesson_passes': get_lesson_info(4)
    }


def get_learning_items(id_):
    item = LearningProcess.query.get(id_)
    if not item:
        return {}
    return {
        'text': item.text
    }


def get_learning_items_dict():
    return {
        'step_1': get_learning_items(1)['text'],
        'step_2': get_learning_items(2)['text'],
        'step_3': get_learning_items(3)['text'],
        'step_4': get_learning_items(4)['text'],
        'step_5': get_learning_items(5)['text'],
        'step_6': get_learning_items(6)['text'],
        'step_7': get_learning_items(7)['text']
    }


def get_text_data(id_):
    data = TextData.query.get(id_)
    if not data:
        return {}
    return {
        'text': data.text
    }


def get_textdata():
    return {
        'site_header': get_text_data(1)['text'],
        'site_subheader': get_text_data(2)['text'],
        'button_text': get_text_data(3)['text'],
        'section2_title': get_text_data(4)['text'],
        'section2_content': get_text_data(5)['text'],
        'about_title': get_text_data(6)['text'],
        'about_content': get_text_data(7)['text'],
        'section4_title': get_text_data(8)['text'],
        'section4_content': get_text_data(9)['text'],
        'section4_list_title': get_text_data(10)['text'],
        'section5_title': get_text_data(11)['text'],
        'section5_text1': get_text_data(12)['text'],
        'section5_text2': get_text_data(13)['text']
    }


@app.route('/')
def index():
    prices = get_prices()
    textdata = get_textdata()
    learningitems = get_learning_items_dict()
    return render_template('index.html', prices=prices, textdata = textdata, learningitems = learningitems)


@app.route('/callback', methods=['GET', 'POST'])
def callback():
    prices = get_prices()
    textdata = get_textdata()
    learningitems = get_learning_items_dict()
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

            # mail.send(msg)
            print("Email sent")
            
        except Exception as e:
            print(e)
            flash('Произошла ошибка при отправке. Попробуйте позже.', 'error')
        
        form_type = request.form.get('form_type')
        if form_type == "up_callback":
            return redirect(url_for('index') + '#up_callback-form')
        elif form_type == "down_callback":
            flash('Спасибо! Ваша заявка отправлена.', 'success_down_callback')
            return redirect(url_for('index') + '#down_callback-form')

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
