import re
from flask import Flask, redirect, request, render_template, send_from_directory, session, url_for,  flash
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from dao.ChapterDao import ChapterDao
from dao.HistoryOfIssuanceDao import HistoryOfIssuanceDao
from dao.HistoryRequestDao import HistoryRequestDao
from dao.AccountDao import AccountDao
from constant.Constant import ALLOWED_EXTENSIONS_FOR_AVATARS, ALLOWED_EXTENSIONS_FOR_BOOKS, UPLOAD_FILE_FOLDER, UPLOAD_IMAGE_FOLDER
from constant.RoutConstant import RouteConstants
from dao.BookDao import BookDao
from dao.CommonDao import CommonDao
import os
import uuid
import datetime

from database.LibraryDatabase import LibraryDatabase
from service.BookService import BookService
from service.AccountService import AccountService
from service.HistoryOfIssuanceService import HistoryOfIssuanceService
from service.HistoryRequestService import HistoryRequestService
from service.ChapterService import ChapterService

'''
Файл запускающий сайт и содержащий все роуты этого сайта
'''

global app

app = Flask(__name__)
app.secret_key = "secret"
db = LibraryDatabase()
book_service = BookService(BookDao(db))
account_service = AccountService(AccountDao(db))
history_request_service = HistoryRequestService(HistoryRequestDao(db))
history_of_issuance_service = HistoryOfIssuanceService(HistoryOfIssuanceDao(db))
chapter_service = ChapterService(ChapterDao(db))

def download_avatar(avatar_field: str):
    response = {"data": "", "error": ""}
    if avatar_field in request.files:
        file = request.files[avatar_field]
        if file and allowed_file(file.filename, ALLOWED_EXTENSIONS_FOR_AVATARS):
            avatar_filename = secure_filename(file.filename)
            unique_id = str(uuid.uuid4())
            file_extension = avatar_filename.rsplit('.', 1)[1].lower()
            new_avatar_filename = f"{unique_id}.{file_extension}"
            response["data"] = new_avatar_filename
        else:
            response["error"] = "Неправильный тип файла"
    else:
        response["error"] = "Аватарка не загружена"
    return response

def allowed_file(filename, types):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in types

def delete_file(filename: str, path):
    file_path = path+f"/{filename}"
    if os.path.exists(file_path):
        os.remove(file_path)
        
def is_older_than_five_years(birth_date):
    birth = datetime.datetime.strptime(birth_date, '%Y-%m-%d')
    today = datetime.datetime.today()
    age = today.year - birth.year
    if today.month < birth.month or (today.month == birth.month and today.day < birth.day):
        age -= 1
    return age >= 5

@app.route(RouteConstants.SEARCH_PATH)
@app.route(RouteConstants.SEARCH_PATH_WITH_PAGE)
def search(page=1):
    per_page = 10
    text = request.args.get('search_field')
    if text == None:
        text = ""
    count_books = book_service.get_count_books_by_title(text)
    books = book_service.get_all_by_title(text, per_page, page)
    total_pages = (count_books + per_page - 1) // per_page
    return render_template('search.html', head_title='Поиск книг', books=books, page=page, total_pages=total_pages, textField=text)

@app.route(RouteConstants.HOME_PATH, methods=['GET'])
def index():
    return redirect("search")

@app.route(RouteConstants.LOGIN_PATH, methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            flash('Неправильный формат email.')
            return redirect(url_for('login'))
        
        account = account_service.login(email, password)
        
        if account == None:
            flash('Неправильный ввод данных')
            return redirect(url_for('login'))
        if account[7] == 3:
            session['chapter_id'] = chapter_service.get_librarian_chapter(account[0])
        session['user_id'] = account[0]
        session['avatar'] = account[8]
        session['role'] = account[7]
        return redirect(url_for('index'))
            
    return render_template('login.html', head_title='Вход в аккаунт')

@app.route(RouteConstants.REGISTER_PATH, methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        phone = request.form.get('phone')
        birth = request.form.get('birth')
        password = request.form.get('new_password')
        password_hash = generate_password_hash(password)
        
        if account_service.exists(email):
            flash('Пользователь с таким email уже существует. Пожалуйста, попробуйте другой email.')
            return redirect(url_for('register'))

        if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            flash('Неправильный формат email.')
            return redirect(url_for('register'))

        phone_pattern = re.compile(r'^\d{11}$')
        if not phone_pattern.match(phone):
            flash('Номер телефона должен содержать 11 цифр.')
            return redirect(url_for('register'))

        if not is_older_than_five_years(birth):
            flash('Вы должны быть старше 5 лет для регистрации.')
            return redirect(url_for('register'))

        response = download_avatar("avatar")
        if response["error"] != "":
            flash(response["error"])
            return redirect(url_for('register'))
        else:
            file = request.files['avatar']
            filepath = os.path.join(UPLOAD_IMAGE_FOLDER, response["data"])
            file.save(filepath)
            
        account_service.registration(firstname, lastname, email, phone, birth, password_hash, response["data"])
        return redirect(url_for('login'))
        
    return render_template('register.html', head_title="Регистрация")

@app.route(RouteConstants.LOGOUT_PATH)
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    session.pop('chapter', None)
    return redirect(url_for('index'))

@app.route(RouteConstants.BOOK_PATH, methods=['GET', 'POST'])
def book(book_id):
    book = book_service.get_by_id(book_id)
    chapter = chapter_service.get_chapter_by_id(book[7])
    
    if book is None:
        return redirect(url_for('search'))
    
    if request.method == 'POST':
        history_request_service.add_history_request(book_id, session.get('user_id'))
        return redirect(url_for('book', book_id=book_id))
    
    status = ""
    if history_request_service.exists(book_id, session.get('user_id')): 
        status = "Запрос отправлен"
    elif history_of_issuance_service.exists_in_history(book_id, session.get('user_id')):
        status = "В наличии"
        
    return render_template('book.html', head_title="Информация о книге", book = book, status=status, chapter_id=chapter[1])

@app.route(RouteConstants.PROFILE_PATH, methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session.get('user_id')
    account_role = session.get('role')
    account = account_service.get_account_by_id(user_id)
    
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        phone = request.form.get('phone')
        birth = request.form.get('birth')
        new_password = request.form.get('new_password')
        file_field = "new_avatar"
        filename = ""
        
        if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            flash('Неправильный формат email.')
            return redirect(url_for('register'))

        phone_pattern = re.compile(r'^\d{11}$')
        if not phone_pattern.match(phone):
            flash('Номер телефона должен содержать 11 цифр.')
            return redirect(url_for('register'))

        if not is_older_than_five_years(birth):
            flash('Вы должны быть старше 5 лет для регистрации.')
            return redirect(url_for('register'))
        
        if new_password == "":
            new_password = account[9]
        else:
            new_password = generate_password_hash(new_password)
            
        response = download_avatar(file_field)
        
        if response["data"] == "":
            filename = account[8]
        else:
            file = request.files[file_field]
            filepath = os.path.join(UPLOAD_IMAGE_FOLDER, response["data"])
            filename = response["data"]
            session['avatar'] = filename
            file.save(filepath)
            delete_file(account[8], UPLOAD_IMAGE_FOLDER)
        
        account_service.update_account(user_id, firstname, lastname, email, phone, birth, new_password, filename)
        flash('Данные успешно обновлены!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('profile.html', head_title="Профиль", account=account, account_role=account_role)

@app.route(RouteConstants.LIBRIRAN_BOOKS_PATH, methods=['GET', 'POST'])
@app.route(RouteConstants.LIBRIRAN_BOOKS_PATH_WITH_PAGE, methods=['GET', 'POST'])
def librarian_books(page=1):
    per_page = 5
    account_id = session.get('user_id')
    
    text = request.args.get('search_field')
    if text == None:
        text = ""
        
    chapter = chapter_service.get_librarian_chapter(account_id)
    chapter_id = chapter[0]
    chapter_title = chapter[1]
    
    count_books = book_service.get_count_books_by_chapter(chapter_id)
    
    books = book_service.get_all_by_chapter_pagable(text, chapter_id, per_page, page)
    total_pages = (count_books + per_page - 1) // per_page
    if books == []:
        return render_template('librarian_books.html', head_title="Список книг по разделам", books=None, page=page, total_pages=total_pages, textField=text)
    return render_template('librarian_books.html', head_title="Список книг по разделам", chapter_title=chapter_title, books=books, page=page, total_pages=total_pages, textField=text)

@app.route(RouteConstants.EDIT_BOOK_PATH, methods=['POST', 'GET'])
def edit_book(book_id):
    book = book_service.get_by_id(book_id)
    
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        public_year = request.form.get('public_year')
        isbn = request.form.get('isbn')
        image = request.form.get('image')
        description = request.form.get('description')
        unique_filename = book[6]
        
        if book_service.exist_isbn_by_book_id(isbn, book_id):
            flash("Такой номер книги уже есть", "danger")
            return redirect(url_for('edit_book', book_id=book_id))
        
        file_field = "file"
        if file_field in request.files:
            file = request.files[file_field]
            if file.filename != '':
                if allowed_file(file.filename, ALLOWED_EXTENSIONS_FOR_BOOKS):
                    if unique_filename:
                        existing_file_path = os.path.join(UPLOAD_FILE_FOLDER, unique_filename)
                        if os.path.isfile(existing_file_path):
                            os.remove(existing_file_path)
                            flash('Существующий файл удален.', 'info')
                    unique_filename = f"{uuid.uuid4()}.{file.filename.rsplit('.', 1)[-1].lower()}"
                    file.save(os.path.join(UPLOAD_FILE_FOLDER, unique_filename))
                    flash('Файл успешно загружен!')
                else:
                    flash('Недопустимый файл. Пожалуйста, загрузите файл с расширением .pdf или .docx.')
                
        book_service.update_book(book_id, title, author, public_year, isbn, image, unique_filename, session.get('chapter_id')[0], description)
        flash('Данные успешно обновлены!', 'success')
        return redirect(url_for('edit_book', book_id=book_id))
        
    return render_template("edit_book.html", head_title="Редактирование книги", book=book, book_id=book_id)

@app.route(RouteConstants.DELETE_BOOK_PATH, methods=['POST'])
def delete_book(book_id):
    if request.method == 'POST':
        book = book_service.get_by_id(book_id)
        book_file_path = book[6]
        book_service.delete_book_by_id(book_id)
        delete_file(book_file_path, UPLOAD_FILE_FOLDER)
        flash('Книга успешно удалена')
    return redirect(url_for('librarian_books'))

@app.route(RouteConstants.ADD_BOOK_PATH, methods=['POST', 'GET'])
def add_book():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        public_year = request.form.get('public_year')
        isbn = request.form.get('isbn')
        image = request.form.get('image')
        description = request.form.get('description')
        file_field = "file"
        unique_filename = ""
        
        if book_service.exist_isbn(isbn):
            flash("Такой номер книги уже есть", "danger")
            return redirect(url_for('add_book'))
        
        if file_field in request.files:
            file = request.files[file_field]
            if file.filename != '':
                if allowed_file(file.filename, ALLOWED_EXTENSIONS_FOR_BOOKS):
                    unique_filename = f"{uuid.uuid4()}.{file.filename.rsplit('.', 1)[-1].lower()}"
                    file.save(os.path.join(UPLOAD_FILE_FOLDER, unique_filename))
                    flash('Файл успешно загружен!')
                else:
                    flash('Недопустимый файл. Пожалуйста, загрузите файл с расширением .pdf или .docx.')
                    
        book_service.insert_book(title, author, public_year, isbn, image, unique_filename, session.get('chapter_id')[0], description)
        flash('Книга успешно добавлена')
        return redirect(url_for('librarian_books'))
    
    return render_template("add_book.html", head_title="Добавление книги")

@app.route(RouteConstants.REQUEST_BOOK_PATH, methods=['GET', 'POST'])
@app.route(RouteConstants.REQUEST_BOOK_PATH_WITH_PAGE, methods=['GET', 'POST'])
def request_books(page=1):
    per_page = 5
    
    if request.method == 'POST':
        if 'rejection_history_request_id' in request.form:
            history_request_service.delete_history_request_by_history_request_id(request.form.get('rejection_history_request_id'))
            flash('Запрос отменён!')
            return redirect(url_for('request_books'))
        history_request_id = request.form.get('history_request_id')
        account_id = request.form.get('account_id')
        book_id = request.form.get('book_id')
        
        history_request_service.delete_history_request_by_history_request_id(history_request_id)
        history_of_issuance_service.add_history_issuence(account_id, book_id)
        
        flash('Запрос одобрен!')
        return redirect(url_for('request_books'))
    chapter_id = session.get('chapter_id')
    
    count_history_request = history_request_service.get_count_history_request_by_book_ids(chapter_id[0])
    history_request = history_request_service.get_history_request_by_book_ids(chapter_id[0], per_page, page)
    if history_request == []:
        return render_template('request_books.html', head_title="Запросы книг для одобрения",  history_request=None)
    total_pages = (count_history_request + per_page - 1) // per_page
    
    return render_template('request_books.html', head_title="Запросы книг для одобрения", history_request=history_request, page=page, total_pages=total_pages)

@app.route(RouteConstants.HISTORY_ISSUENCE_PATH, methods=['GET', 'POST'])
@app.route(RouteConstants.HISTORY_ISSUENCE_PATH_WITH_PAGE, methods=['GET', 'POST'])
def history_issuance(page=1):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    per_page = 10
    account_id = session.get('user_id')
    count_history_of_issuance = history_of_issuance_service.get_count_history_issuence(account_id)
    books = history_of_issuance_service.get_history_issuence_by_account_id(account_id)
    total_pages = (count_history_of_issuance + per_page - 1) // per_page
    
    if books == []:
        return render_template('history_issuance.html', head_title="Ваши книги", books=None, account_id=account_id, page=page, total_pages=total_pages)

    indexes = [book[2] for book in books]
    index_string = ', '.join(map(str, indexes))
    books = history_of_issuance_service.get_history_request_by_book_ids(index_string, account_id, per_page, page)
    
    if 'book_id' in request.form:
        book_id = request.form['book_id']
        
        history_of_issuance_service.update_history_issuence_is_read(account_id, book_id, True)
        
        return redirect(url_for('history_issuance'))
        
    elif 'file_path' in request.form:
        file_path = request.form['file_path']
        return redirect(url_for('download_file', filename=file_path))
    
    return render_template('history_issuance.html', head_title="Ваши книги", books=books, account_id=account_id, page=page, total_pages=total_pages)

@app.route(RouteConstants.SHARE_PAGE_PATH, methods=['GET', 'POST'])
@app.route(RouteConstants.SHARE_PAGE_PATH_WITH_PAGE, methods=['GET', 'POST'])
def share_page(page=1):
    per_page = 10
    
    account_id = request.args.get('reader')
    account = account_service.get_account_by_id(account_id)
    
    if not account:
        return redirect(url_for('search'))
    
    count_history_of_issuance = history_of_issuance_service.get_count_history_issuence(account_id)
    books = history_of_issuance_service.get_history_issuence_by_account_id(account_id)
    total_pages = (count_history_of_issuance + per_page - 1) // per_page
    
    if books == []:
        return render_template('share_page.html', head_title="История чтения", books=None, firstname=account[1],
                           lastname=account[2], account_id=account_id, page=page, total_pages=total_pages)

    indexes = [book[2] for book in books]
    index_string = ', '.join(map(str, indexes))
    books = history_of_issuance_service.get_history_request_by_book_ids(index_string, account_id, per_page, page)
    
    return render_template('share_page.html', head_title="История чтения", books=books, firstname=account[1],
                           lastname=account[2], account_id=account_id, page=page, total_pages=total_pages)

@app.route(RouteConstants.DOWNLOAD_FILE_PATH, methods=['GET'])
def download_file(filename):
    return send_from_directory(UPLOAD_FILE_FOLDER, filename, as_attachment=True)

db.init_db()
os.makedirs(UPLOAD_IMAGE_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FILE_FOLDER, exist_ok=True)

if __name__ == '__main__':
    app.run(debug=True)
