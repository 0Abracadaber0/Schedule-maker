window.onload = checkAuthentication;
function openTab(evt, tabName) {
    let i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

function checkAuthentication() {
    const isUserAuthenticated = false;

    if (isUserAuthenticated) {
        document.getElementById("Register_button").style.display = "none";
        document.getElementById("Login_button").style.display = "none";
    } else {
        document.getElementById("Classes_button").style.display = "none";
        document.getElementById("Lessons_button").style.display = "none";
        document.getElementById("Teachers_button").style.display = "none";
        document.getElementById("Subjects_button").style.display = "none";
    }
}