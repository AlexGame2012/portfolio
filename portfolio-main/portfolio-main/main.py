#Импорт
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель базы данных
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    text = db.Column(db.Text, nullable=False)

# Создание базы данных
with app.app_context():
    db.create_all()

@app.route('/admin',  methods=['GET', 'POST'])
def admin():
    message = ''
    message2 = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'Admin' and password == 'AlexGame2012' or username == 'root' and password == 'AlexRoot':
            message = ''
            message2 = ''
            return redirect(url_for('panel'))
        else:
            message = 'Ошибка!'
            message2 = 'Неверный имя пользователя или пароль.'
    return render_template('login.html', message=message, message2=message2)

#Запуск страницы с контентом
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/panel')
def panel():
    comments =  Feedback.query.all()
    return render_template('panel.html', comments=comments)

#Динамичные скиллы
@app.route('/', methods=['GET', 'POST'])
def process_form():
    if request.method == 'POST':
        email = request.form.get('email', False)
        text = request.form.get('text', False)
        new_feedback = Feedback(email=email, text=text)
    db.session.add(new_feedback)
    db.session.commit()
    button_python = request.form.get('button_python')
    button_html = request.form.get('button_html')
    button_discord = request.form.get('button_discord')
    button_db = request.form.get('button_db')
    button_js = request.form.get('button_js')
    return render_template('index.html', text=text, email=email, button_python=button_python, button_html=button_html, button_discord=button_discord, button_db=button_db, button_js=button_js)

if __name__ == '__main__':
    app.run(debug=True)
