import { getCSRFToken } from './getCSRF.js';

document.querySelectorAll(".order").forEach(orderBlock => {
    let totalPrice = 0;
    let totalCount = 0;

    orderBlock.querySelectorAll(".order-item").forEach(item => {
        const price = parseInt(item.querySelector("[data-price]").textContent.split(" ")[0]);
        const count = parseInt(item.querySelector("[data-count]").textContent.split(" ")[0]);
        totalPrice += price * count;
        totalCount += count;
    });

    const totalSumBlock = orderBlock.querySelector(".order-total-sum");
    totalSumBlock.textContent = `${totalPrice} ₽`;
    const totalCountBlock = orderBlock.querySelector(".order-total-count");
    if (totalCount % 100 >= 11 && totalCount % 100 <= 19) {
        totalCountBlock.textContent = `${totalCount} товаров`;
    }
    else {
        const lastDigit = totalCount % 10;
        if (lastDigit === 1) totalCountBlock.textContent = `${totalCount} товар`;
        else if (lastDigit >= 2 && lastDigit <= 4) totalCountBlock.textContent = `${totalCount} товара`;
        else totalCountBlock.textContent = `${totalCount} товаров`;
    }
});


document.querySelectorAll('.show-more-button').forEach(button => {
    button.addEventListener('click', () => {
        const order = button.closest('.order');
        const orderItems = order.querySelector('.order-items');

        orderItems.classList.toggle('order-items_open');

        button.classList.toggle('show-more-button_active');
    });
});


document.querySelector("#logout-button").addEventListener("click", async function() {
    const dialog = confirm("Вы уверены, что хотите выйти?");
    if (dialog) {
        try {
            const response = await fetch("/logout/", { 
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken(),
                }
            });

            if (response.ok) {
                window.location.replace('/');
            } else {
                const error = await response.json();
                console.error(`Ошибка: ${error.message}`);
            }
        } catch (err) {
            console.error("Ошибка:", err);
        }
    };
});


if (window.innerWidth <= 768) {
    document.querySelectorAll('.product__author').forEach(element => element.remove());
}