
from dao.BookDao import BookDao
from dao.CommonDao import CommonDao

'''
класс sevice отвечает за работу с dao и данными book
'''
class BookService:
    
    def __init__(self, dao: BookDao):
        super().__init__()
        self.dao = dao
        
    def get_all_by_title(self, title: str, per_page: str, page: str):
        return self.dao.select_all_by_title(title, per_page, page)
    
    def get_count_books_by_title(self, title:str):
        return self.dao.count_books_by_title(title)
    
    def get_by_id(self, book_id: str):
        return self.dao.select_by_id(book_id)
    
    def get_all_by_chapter_pagable(self, title: str, chapter_id: str, per_page: str, page: str):
        return self.dao.select_with_pagable_all_by_chapter(title, chapter_id, per_page, page)
    
    def exist_isbn_by_book_id(self, isbn: str, book_id: str):
        return self.dao.count_books_with_cur_isbn_by_book_id(isbn, book_id)
    
    def exist_isbn(self, isbn: str):
        return self.dao.count_books_with_cur_isbn(isbn)
    
    def get_all_by_chapter(self, chapter_id: str):
        return self.dao.select_by_chapter(chapter_id)
    
    def get_count_books_by_chapter(self, chapter_id: str):
        return self.dao.count_books_with_where(chapter_id)
    
    def update_book(self, book_id: str, title: str, author: str, public_year: str, isbn: str, image: str, file_path: str, chapter_id: str, description: str):
        book_data = {
            "title": title,
            "author": author,
            "public_year": public_year,
            "isbn": isbn,
            "image": image,
            "file_path": file_path,
            "chapter_id": chapter_id,
            "description": description
        }
        self.dao.update_book_by_id(book_data, book_id)
        
    def delete_book_by_id(self, book_id: str):
        self.dao.delete_by_id(book_id)
        
    def insert_book(self, title: str, author: str, public_year: str, isbn: str, image: str, file_path: str, chapter_id: str, description: str):
        book_data = {
            "title": title,
            "author": author,
            "public_year": public_year,
            "isbn": isbn,
            "image": image,
            "file_path": file_path,
            "chapter_id": chapter_id,
            "description": description
        }
        self.dao.insert(book_data)