// todo dark mode toggle
function ToggleDarkMode () {
    var maincontent = document.getElementById("maincontent");
    var icon = document.getElementById("style-toggle");

    if (maincontent.classList.contains('light')) {
        maincontent.classList.add('dark');
        maincontent.classList.remove('light');
        icon.classList.add('fa-moon-o');
        icon.classList.remove('fa-sun-o');
        //document.body.style.backgroundImage= "linear-gradient(90deg, #ff8a00, #e52e71)"
        document.body.style.backgroundColor= "#222"
    } else {
        maincontent.classList.add('light');
        maincontent.classList.remove('dark');
        icon.classList.remove('fa-moon-o');
        icon.classList.add('fa-sun-o');
        document.body.style.backgroundColor= "#FFF"
    }
}