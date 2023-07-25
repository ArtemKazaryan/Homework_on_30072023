
# Домашняя работа на 30.07.2023


import os
import sqlite3
from flask import Flask, render_template, request, flash, session, redirect, url_for, abort
from DataBase import DataBase

DATABASE = '/tmp/financial.db'
DEBUG = True  # включаем режим отладки в режиме работы main файла
SECRET_KEY = '123456789'  # Напрямую прописываем секретный ключ для функционирования сессии session

app = Flask(__name__) # Создаём приложение с помощью класса Flask библиотеки flask

app.config.from_object(__name__)  # Объявляем конфигурирование нашего приложения

app.config.update({'DATABASE': os.path.join(app.root_path, 'financial.db')})  # Обновляем конфигурацию нашего приложения
# с заданием имени базы данных, с которой приложение будет работать

# Создаём функцию для создания подключения нашего приложения к базе данных с помощью sqlite3 библиотеки
def connect_db():
    con = sqlite3.connect(app.config['DATABASE'])
    con.row_factory = sqlite3.Row   # Команда `con.row_factory = sqlite3.Row` устанавливает фабрику объектов строк
    # для объекта подключения к базе данных SQLite. По умолчанию, при выполнении запросов к базе данных SQLite,
    # результаты возвращаются в виде кортежей. Однако, установка `con.row_factory = sqlite3.Row` позволяет
    # получать результаты запросов в виде объектов `Row`, которые предоставляют доступ к данным по их именам столбцов.
    # Таким образом, после установки данной команды, можно получать значения из результата запроса,
    # обращаясь к ним по именам столбцов, что упрощает и улучшает читаемость кода.
    return con

# Создаём функцию для создания базы данных, извлекая скрипт команд по созданию таблиц из файла sq_db.sql
def create_db():
    db = connect_db()
    with open('sq_db.sql', 'r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


# Создаём ссылочный маршрутизатор нашего приложения, под управлением которого находится функция, отвечающая за:
@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    db_con = connect_db()  # создание соединения с базой данных
    db = DataBase(db_con)  # создание объекта класса DataBase, имеющего аттрибут курсора и доступ к разнообразным
    # методам работы с ним.

    # проверку условий запуска html-шаблона html-файла index.html
    if request.method == 'POST':
        if len(request.form['date']) > 1:
            flash('Транзакция успешно зарегистрирована!', category='success')

    # возврат команды на выполнение визуализации(рендеринга, отображения) шаблона в index.html
    # с дополнительным указанием значений локальных jinja-инициализированных рендеринг-переменных
    return render_template("index.html", title='Здесь Вы можете посмотреть содержимое списка транзакций',
                           transacts=db.get_transacts(), menu=db.get_menu())


# Создаём ссылочный маршрутизатор нашего приложения для перехода на страницу ввода транзакции, аналогичный вышеуказанному
@app.route('/add_transact', methods=['GET', 'POST'])
def add_transact():
    db_con = connect_db()
    db = DataBase(db_con)

    if request.method == 'POST':
        if len(request.form['income_expenditure']) > 0 and len(request.form['product']) > 0:
            res = db.add_transact(request.form['date'], request.form['income_expenditure'], request.form['product'],
                                  request.form['price'], request.form['quantity'])
            if res:
                flash('Транзакция добавлена успешно!', category='success')
            else:
                flash('Ошибка добавления транзакции!', category='error')
        else:
            flash('Ошибка добавления транзакции!', category='error')

    return render_template('add_transact.html', title='Добавление транзакции', menu=db.get_menu())


# Попытка прописать обработчик для удаления из БД строки по айдишнику
# @app.route('/index', methods=['GET', 'POST'])
# def delete_transact():
#     db_con = connect_db()
#     db = DataBase(db_con)
#
#     if request.method == 'POST':
#         res = request.form['id']
#         print(res)
#         flash('Транзакция успешно удалена!', category='error')
#         db.delete_transact(res)
#
#     return render_template("index.html", title='Здесь Вы можете посмотреть содержимое списка транзакций',
#                            transacts=db.get_transacts(), menu=db.get_menu())


# Создаём ссылочный маршрутизатор нашего приложения для вывода списка транзакций
@app.route('/transact/<transact_id>')
def show_transact(transact_id):
    db_con = connect_db()
    db = DataBase(db_con)

    product, transact = db.get_transact(transact_id)
    if not product:
        abort(404)

    return render_template('transact.html', title=title, transact=transact, menu=db.get_menu())


# Создаём ссылочный маршрутизатор нашего приложения, аналогичный вышеуказанному
@app.route('/about')
def about():
    db_con = connect_db()
    db = DataBase(db_con)
    return render_template("about.html", menu=db.get_menu())


# Создаём ссылочный маршрутизатор нашего приложения, аналогичный вышеуказанному
@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    db_con = connect_db()
    db = DataBase(db_con)
    context = {}
    if request.method == 'POST':
        if len(request.form['username']) > 1:
            flash('Сообщение отправлено успешно!', category='success')
        else:
            flash('Ошибка отправки!', category='error')
        context = {
            'username': request.form['username'],
            'phone': request.form['phone'],
            'message': request.form['message']
        }
    return render_template("contacts.html", **context, title='Обратная связь', menu=db.get_menu())


# Создаём ссылочный маршрутизатор нашего приложения, аналогичный вышеуказанному
@app.route('/profile/<username>')
def profile(username):
    db_con = connect_db()
    db = DataBase(db_con)
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    return render_template("profile.html", title=f'Авторизация пользователя {username} уже произведена', menu=db.get_menu())


# Создаём ссылочный маршрутизатор нашего приложения, аналогичный вышеуказанному
@app.route('/login', methods=['GET', 'POST'])
def login():
    db_con = connect_db()
    db = DataBase(db_con)
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == 'admin' \
                                  and request.form['password'] == '123456789':
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))
    return render_template('login.html', title='Авторизация', menu=db.get_menu())


# Создаём обработчик ошибок 400 в работе маршрутизаторов нашего приложения
@app.errorhandler(400)
def page_not_found(error):
    return render_template('pageERR.html', title='Неверный запрос', menu=db.get_menu(), error=error), 400


# Создаём обработчик ошибок 401 в работе маршрутизаторов нашего приложения
@app.errorhandler(401)
def page_not_found(error):
    return render_template('pageERR.html', title='Нет прав', error=error), 401


# Создаём обработчик ошибок 404 в работе маршрутизаторов нашего приложения
@app.errorhandler(404)
def page_not_found(error):
    return render_template('pageERR.html', title='Страница не найдена', error=error), 404


# Прописываем условие активации функции создания базы данных и метода запуска нашего flask-приложения (метод ru)
if __name__ == '__main__':
    create_db()
    app.run()

