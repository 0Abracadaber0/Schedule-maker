document.querySelector("form").addEventListener("submit", function (event) {
    event.preventDefault(); // Останавливаем отправку формы, чтобы обработать валидацию

    // Получаем значения полей
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;
    var confirm_password = document.getElementById("password_confirm").value;

    var isValid = true; // Переменная для отслеживания, прошла ли форма валидацию

    // Скрываем все сообщения об ошибках перед валидацией
    document.getElementById("email-error-message").style.display = "none";
    document.getElementById("password-confirm-error-message").style.display = "none";
    document.getElementById("email").classList.remove("error");
    document.getElementById("password_confirm").classList.remove("error");

    // Проверяем email
    var emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (!emailPattern.test(email)) {
        document.getElementById("email-error-message").style.display = "block";
        document.getElementById("email-error-message").textContent = "Введите корректный email";
        document.getElementById("email").classList.add("error");
        isValid = false;
    }

    // Проверяем совпадение паролей
    if (password !== confirm_password) {
        document.getElementById("password-confirm-error-message").style.display = "block";
        document.getElementById("password-confirm-error-message").textContent = "Пароли не совпадают";
        document.getElementById("password_confirm").classList.add("error");
        isValid = false;
    }

    // Если все проверки пройдены, отправляем форму
    if (isValid) {
        // Форма отправляется, только если валидация прошла успешно
        event.target.submit();
    }
});
