/* 
* Вызывает диалоговое окно, подтверждающее намерение удалить книгу, после чего отправляет на rout удаляющий книгу
*/
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.delete-button').forEach(button => {
        button.addEventListener('click', function() {
            const bookId = this.closest('form').id.split('-')[2];
            confirmDeleteBook(bookId);
        });
    });
});

function confirmDeleteBook(bookId) {
    if (confirm("Вы уверены, что хотите удалить эту книгу?")) {
        const form = document.getElementById(`delete-form-${bookId}`);
        if (form) {
            form.submit();
        }
    }
}