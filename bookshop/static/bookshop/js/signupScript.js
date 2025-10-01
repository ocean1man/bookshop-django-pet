import { getCSRFToken } from './getCSRF.js';

let loginButton = document.querySelector("#send-button");
loginButton.addEventListener("click", async function (event) {

    event.preventDefault();

    const username = document.querySelector('#username').value;
    const password = document.querySelector('#password').value;
    const confirmPassword = document.querySelector('#confirm-password').value;

    if (checkPassword(password)) {

        if (password !== confirmPassword) {
            alert("Пароли не совпадают!");
            return;
        }

        try {
            const response = await fetch("/signup/", { 
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
                if (result.message === "exists") alert("Пользователь с таким именем уже существует!");
                else{ 
                    alert("Вы успешно зарегистрированы!");
                    window.location.replace('/');
                };
            } else {
                const error = await response.json();
                console.error(`Ошибка: ${error.message}`);
            }
        } catch (err) {
            console.error("Ошибка:", err);
        }
    } else {
        alert("Пароль должен быть длиной не менее 8 символов, содержать хотя бы одну заглавную букву, одну строчку букву и одну цифру!");
    }
});


function checkPassword(password) {
    if (password.length < 8) {
        return false;
    }
    
    const hasUpperCase = /[A-ZА-Я]/.test(password);
    const hasLowerCase = /[a-zа-я]/.test(password);
    const hasDigit = /\d/.test(password);
    
    return hasUpperCase && hasLowerCase && hasDigit;
};