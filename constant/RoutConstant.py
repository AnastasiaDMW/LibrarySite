'''
Константы роутов для навигации по страницам
'''
class RouteConstants:
    SEARCH_PATH = "/search"
    SEARCH_PATH_WITH_PAGE = "/search/page/<int:page>"
    HOME_PATH = "/"
    LOGIN_PATH = "/login"
    REGISTER_PATH = "/register"
    LOGOUT_PATH = "/logout"
    BOOK_PATH = "/search/books/<int:book_id>"
    PROFILE_PATH = "/profile"
    LIBRIRAN_BOOKS_PATH = "/profile/librarian_books"
    LIBRIRAN_BOOKS_PATH_WITH_PAGE = "/profile/librarian_books/page/<int:page>"
    EDIT_BOOK_PATH = "/profile/librarian_books/edit_book/<int:book_id>"
    DELETE_BOOK_PATH = "/profile/librarian_books/delete_book/<int:book_id>"
    ADD_BOOK_PATH = "/profile/librarian_books/add_book"
    REQUEST_BOOK_PATH = "/profile/request_books"
    REQUEST_BOOK_PATH_WITH_PAGE = "/profile/request_books/page/<int:page>"
    HISTORY_ISSUENCE_PATH = "/history_issuance"
    HISTORY_ISSUENCE_PATH_WITH_PAGE = "/history_issuance/page/<int:page>"
    SHARE_PAGE_PATH = "/share_page"
    SHARE_PAGE_PATH_WITH_PAGE = "/share_page/page/<int:page>"
    DOWNLOAD_FILE_PATH = "/download/<path:filename>"