function setDisplayMode() {
    body = document.querySelector('body');
    darkModeButton = document.querySelector('#darkModeButton');

    if (!(checkCookie("darkMode"))) {
        setCookie("darkMode", 0, 365);
    }

    if (getCookie("darkMode") == 1) {
        switchDarkMode();
    }
}

function switchDarkMode() {
    body = document.querySelector('body');
    darkModeButton = document.querySelector('#darkModeButton');

    if (body.classList.contains("bg-light")) {
        body.classList.remove("bg-light");
        body.classList.remove("text-dark");
        body.classList.add("bg-dark");
        body.classList.add("text-white");
        darkModeButton.classList.remove("btn-dark");
        darkModeButton.classList.add("btn-light");
        darkModeButton.innerText = "Switch to Light-Mode";

        setCookie("darkMode", 1, 365);
    } else if (body.classList.contains("bg-dark")) {
        body.classList.remove("bg-dark");
        body.classList.remove("text-white");
        body.classList.add("bg-light");
        body.classList.add("text-dark");
        darkModeButton.classList.remove("btn-light");
        darkModeButton.classList.add("btn-dark");
        darkModeButton.innerText = "Switch to Dark-Mode";

        setCookie("darkMode", 0, 365);
    }
}