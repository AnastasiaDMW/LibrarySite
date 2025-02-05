
from dao.CommonDao import CommonDao
from database.LibraryDatabase import LibraryDatabase

'''
класс dao отвечающий за таблицу book в базе данных
'''
class BookDao(CommonDao):
        
    def __init__(self, db: LibraryDatabase):
        super().__init__(db)
        self.count_books_template = 'SELECT COUNT(*) FROM %s'
        self.count_books_with_where_template = 'SELECT COUNT(*) FROM %s WHERE %s'
        
    def _get_table_name(self):
        return 'book'
    
    def count_books_by_title(self, title:str):
        res = self._execute_request_all(self.count_books_with_where_template % (self._get_table_name(), f"LOWER(title) LIKE '%{title.lower()}%'"))[0][0]
        return int(res)
    
    def count_books_with_where(self, chapter_id: str):
        res = self._execute_request_all(self.count_books_with_where_template % (self._get_table_name(), f"chapter_id = {chapter_id}"))[0][0]
        return int(res)
    
    def count_books_with_cur_isbn_by_book_id(self, isbn: str, book_id: str):
        res = self._execute_request_all(self.count_books_with_where_template % (self._get_table_name(), f"isbn = '{isbn}' AND id != {book_id}"))[0][0]
        return int(res)
    
    def count_books_with_cur_isbn(self, isbn: str):
        res = self._execute_request_all(self.count_books_with_where_template % (self._get_table_name(), f"isbn = '{isbn}'"))[0][0]
        return int(res)
    
    def delete_by_id(self, book_id: str):
        self._delete(f"id = {book_id}")
        
    def update_book_by_id(self, data: dict, book_id: str):
        self._update(data, f"id = {book_id}")
        
    def select_with_pagable_all_by_chapter(self, title: str, chapter_id: str, per_page: str, page: str):
        return self._select_with_pageable(f"chapter_id = {chapter_id} and LOWER(title) LIKE '%{title.lower()}%'", per_page, page)
    
    def select_by_id(self, book_id: str):
        books: list = self._select_all(f'id = {book_id}')
        if len(books) > 0:
            return books[0]
        return None
    
    def select_by_chapter(self, chapter_id: str):
        return self._select_all(f"chapter_id = {chapter_id}")
    
    def select_all_by_title(self, title: str, per_page: str, page: str):
        return self._select_with_pageable(f"LOWER(title) LIKE '%{title.lower()}%'", per_page, page)

        
        