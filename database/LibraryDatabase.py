import psycopg2

from constant.Constant import DB_CONFIG, DataDatabase, SchemeDatabase

'''
Класс для настройки базы данных
'''
class LibraryDatabase:

    def __init__(self):
        super().__init__()
    
    def get_db_connection(self):
        return psycopg2.connect(**DB_CONFIG)

    def init_db(self):
        conn = self.get_db_connection()
        cur = conn.cursor()
        
        self.create_tables(cur)
        self.insert_data(cur)
        
        conn.commit()
        cur.close()
        conn.close()
        
    def create_tables(self, cur):
        cur.execute(SchemeDatabase.CREATE_ROLE_TABLE)
        cur.execute(SchemeDatabase.CREATE_ACCOUNT_TABLE)
        cur.execute(SchemeDatabase.CREATE_CHAPTER_TABLE)
        cur.execute(SchemeDatabase.CREATE_BOOK_TABLE)
        cur.execute(SchemeDatabase.CREATE_HISTORY_REQUEST_TABLE)
        cur.execute(SchemeDatabase.CREATE_HISTORY_OF_ISSUANCE_TABLE)
        
    def insert_data(self, cur):
        try:
            cur.execute(DataDatabase.INSERT_ROLES)
            cur.execute(DataDatabase.INSERT_LIBRARIAN)
            cur.execute(DataDatabase.INSERT_CHATERS)
            cur.execute(DataDatabase.INSERT_BOOKS_CHAPTER_PSYCHOLOGY)
            cur.execute(DataDatabase.INSERT_BOOKS_CHAPTER_HORROR)
            cur.execute(DataDatabase.INSERT_BOOKS_CHAPTER_DETECTIVE)
        except psycopg2.Error as e:
            print("Данные уже загружены")