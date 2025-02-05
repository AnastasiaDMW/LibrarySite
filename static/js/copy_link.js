/*
*   Функция, которая добавляет ссылку в буффер обмена
*/
function copyToClipboard() {
    var link = document.getElementById("linkInput").value;
    navigator.clipboard.writeText(link).then(function() {
        alert("Ссылка скопирована: " + link);
    }).catch(function(err) {
        console.error('Ошибка при копировании: ', err);
    });
}