let loginButton = document.querySelector("#send-button");
loginButton.addEventListener("click", async function (event) {

    event.preventDefault();

    const username = document.querySelector('#username').value;
    const password = document.querySelector('#password').value;

    try {
        const response = await fetch("/login/", { 
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),
            },
            body: JSON.stringify({
                username: username,
                password: password
            }),
        });

        if (response.ok) {
            const result = await response.json();
            if (result.message === "invalid") alert("Неверное имя пользователя или пароль!");
            else {
                alert("Вы успешно вошли!");
                window.location.replace('/profile/');
            };
        } else {
            const error = await response.json();
            console.error(`Ошибка: ${error.message}`);
        }
    } catch (err) {
        console.error("Ошибка:", err);
    }
});


function getCSRFToken() {
    const cookieValue = document.cookie
      .split("; ")
      .find((row) => row.startsWith("csrftoken="))
      ?.split("=")[1] || "";
    return cookieValue;
}