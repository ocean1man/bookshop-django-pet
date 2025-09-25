function addQuantity() {
    const buttons = document.querySelectorAll(".count__plus");
    buttons.forEach(function(button) {
        button.addEventListener("click", async function () {

            const productId = button.getAttribute("data-product-id");
    
            try {
                const response = await fetch(`/cart/update/${productId}/`, { 
                    method: "PATCH",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCSRFToken(),
                    },
                    body: JSON.stringify({
                        action: "addQuantity"
                    }),
                });
    
                if (response.ok) {
                    updateCart()
                } else {
                    const error = await response.json();
                    console.error(`Ошибка: ${error.message}`);
                }
            } catch (err) {
                console.error("Ошибка добавления товара:", err);
            }
        });
    })
};

addQuantity();


function reduceQuantity() {
    const buttons = document.querySelectorAll(".count__minus");
    buttons.forEach(function(button) {
        button.addEventListener("click", async function () {

            const productId = button.getAttribute("data-product-id");
    
            try {
                const response = await fetch(`/cart/update/${productId}/`, { 
                    method: "PATCH",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCSRFToken(),
                    },
                    body: JSON.stringify({
                        action: "reduceQuantity"
                    }),
                });
    
                if (response.ok) {
                    updateCart()
                } else {
                    const error = await response.json();
                    console.error(`Ошибка: ${error.message}`);
                }
            } catch (err) {
                console.error("Ошибка добавления товара:", err);
            }
        });
    })
};

reduceQuantity();


function deleteProduct() {
    const buttons = document.querySelectorAll("[delete-from-cart]");
    buttons.forEach(function(button) {
        button.addEventListener("click", async function () {

            const productId = button.getAttribute("data-product-id");

            try {
                const response = await fetch(`/cart/delete/${productId}/`, { 
                    method: "DELETE",
                    headers: {
                        "X-CSRFToken": getCSRFToken()
                    }
                });

                if (response.ok) {
                    updateCart();
                } else {
                    const error = await response.json();
                    console.error(`Ошибка: ${error.message}`);
                }
            } catch (err) {
                console.error("Ошибка удаления товара:", err);
            }
        });
    });
}

deleteProduct();


function editWishlist() {
    const buttons = document.querySelectorAll('[add-to-wishlist]');
    buttons.forEach(function(button) {
        button.addEventListener('click', async function() {

            const productId = button.getAttribute('data-product-id');
            let method;
            let url;

            if (button.classList.contains("overlay-button_active")) {
                method = "DELETE";
                url = `/wishlist/delete/${productId}/`;
            } else {
                method = "POST";
                url = `/wishlist/add/${productId}/`;
            }

            try {
                const response = await fetch(url, { 
                    method: method,
                    headers: {
                        "X-CSRFToken": getCSRFToken(),
                    }
                });
        
                if (response.ok) {
                    updateCart();
                } else {
                    const error = await response.json();
                    console.error(`Ошибка: ${error.message}`);
                }
            } catch (err) {
                console.error("Ошибка добавления товара:", err);
            }
        });
    });
};

editWishlist();


function setupCartQuantityHandlers() {
    document.querySelectorAll(".cart-product__price").forEach(countBlock => {

        const minusButton = countBlock.querySelector(".count__minus");
        const plusButton = countBlock.querySelector(".count__plus");
        const display = countBlock.querySelector(".count__quantity");
        const price = countBlock.querySelector(".price");
        const totalPrice = countBlock.querySelector(".total-price");
    
        minusButton.addEventListener("click", () => {
            let currentValue = parseInt(display.textContent);
            if (currentValue > 1) {
                display.textContent = currentValue - 1;
            }
        });
    
        plusButton.addEventListener("click", () => {
            let currentValue = parseInt(display.textContent);
            display.textContent = currentValue + 1;
        });

        totalPrice.textContent = parseInt(display.textContent) * parseInt(price.textContent) + " ₽"
    });
}

setupCartQuantityHandlers();


function calculateTotalPrice() {

    const elements = document.querySelectorAll(".total-price");
    
    let totalSum = 0;
    
    elements.forEach(element => {
        let text = element.textContent.trim();
        
        let value = parseFloat(text.slice(0, -2));
        
        totalSum += value;
    });
    
    const sums = document.querySelectorAll("#total-sum");
    sums.forEach(sum => sum.textContent = totalSum + " ₽");
}

calculateTotalPrice();


function openOrCloseModal() {
    const openButtons = document.querySelectorAll("#open-modal-button");
    const closeButton = document.querySelector("#close-modal-button");
    const modal = document.querySelector(".modal");
    const totalSum = document.querySelector("#total-sum");

    openButtons.forEach(button => {
        button.addEventListener("click", function () {
            if (totalSum.textContent !== "0 ₽") {
                modal.classList.add("modal_open");
            } else {
                alert("Ваша корзина пуста!");
            }
        });
    });

    if (closeButton) {
        closeButton.addEventListener("click", function () {
            modal.classList.remove("modal_open");
        });
    }
}

openOrCloseModal();


function createOrder() {
    const button = document.querySelector("#order-button");
    button.addEventListener("click", async function() {

        fullName = document.querySelector("#full-name").value;
        email = document.querySelector("#email").value;
        mailIndex = document.querySelector("#mail-index").value;

        if (fullName === "" || email === "" || mailIndex === "") return alert("Все поля обязательны для заполнения!")

        try {
            const response = await fetch("/cart/", { 
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken(),
                },
                body: JSON.stringify({
                    fullName: fullName,
                    email: email,
                    mailIndex: mailIndex
                }),
            });
    
            if (response.ok) {
                const result = await response.json();
                if (result.message === "Электронная почта введёна неверно!") return alert(result.message);
                else if (result.message === "Для оформления заказа необходимо войти в свой профиль!") return alert(result.message);
                else {
                    alert(result.message);
                    document.querySelector(".modal").classList.remove("modal_open");
                    updateCart();
                }
            } else {
                const error = await response.json();
                console.error(`Ошибка: ${error.message}`);
            }
        } catch (err) {
            console.error("Ошибка создания заказа:", err);
        }
    })
};

createOrder();


async function updateCart() {
    try {
        const response = await fetch("/cart/");
        if (response.ok) {
            
            const html = await response.text();
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const cartContainer = doc.querySelector("#update-cart");

            document.querySelector("#update-cart").innerHTML = cartContainer.innerHTML;

            deleteProduct();
            editWishlist();
            addQuantity();
            reduceQuantity();
            setupCartQuantityHandlers();
            calculateTotalPrice();
            openOrCloseModal();
            setSmallOrderBox();
        }
    } catch (err) { 
        console.error("Ошибка при обновлении корзины:", err);
    }
};


function getCSRFToken() {
    const cookieValue = document.cookie
      .split("; ")
      .find((row) => row.startsWith("csrftoken="))
      ?.split("=")[1] || "";
    return cookieValue;
};


function setSmallOrderBox() {
    if (window.innerWidth <= 576) {
        document.querySelector('.small-width-order-box').style.display = "block";
    };
}

setSmallOrderBox();