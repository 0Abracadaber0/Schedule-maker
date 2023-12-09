document.querySelector("form").addEventListener("submit", function (event) {
    var password = document.getElementById("password").value;
    var confirm_password = document.getElementById("password_confirm").value;

    if (password !== confirm_password) {
        event.preventDefault();
        document.getElementById("alert").style.display = "block";
    }
});