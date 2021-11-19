window.addEventListener("DOMContentLoaded", function() {
    const registerButton = document.getElementById("register-employee");
    registerButton.addEventListener("click", loadForm);
});

async function fetchHtmlAsText(url) {
    return await (await fetch(url)).text();
}

async function loadForm() {
    const contentDiv = document.getElementById("main");
    contentDiv.innerHTML = await fetchHtmlAsText("register.j2");
}