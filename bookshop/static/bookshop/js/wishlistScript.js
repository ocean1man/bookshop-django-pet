import { getCSRFToken } from './getCSRF.js';

function updateSort() {
    const radioButtons = document.querySelectorAll('input[name="sort"]');
    radioButtons.forEach(function(radio) {
        radio.addEventListener('change', function(event) {

            const form = document.getElementById('sort-form');
            let formData = new FormData(form);
            let sortOrder = event.target.value;
            formData.set('sort', sortOrder);

            let url = new URL(window.location.href);
            
            formData.forEach((value, key) => {
                if (key === 'sort' && value === '') {
                    url.searchParams.delete(key);
                } else {
                    url.searchParams.set(key, value);
                }
            });

            url.searchParams.delete('page'); 

            sendRequest(url)
        });
    });
};

updateSort();


function updateView() {
    const checkbox = document.querySelector('input[name="view"]');
    checkbox.addEventListener('change', function(event) {

        const form = document.getElementById('view-form');
        let formData = new FormData(form);
        let viewType = event.target.checked ? 'row' : '';
        formData.set('view', viewType);

        let url = new URL(window.location.href);
        
        formData.forEach((value, key) => {
            if (key === 'view' && value === '') {
                url.searchParams.delete(key);
            } else {
                url.searchParams.set(key, value);
            }
        });
    
        sendRequest(url)
    })
}

updateView();


function addToCart() {
    const buttons = document.querySelectorAll('#buy-button');
    buttons.forEach(function(button) {
        button.addEventListener('click', async function() {

            const productId = button.getAttribute('data-product-id');

            try {
                const response = await fetch(`/cart/add/${productId}/`, { 
                    method: "POST",
                    headers: {
                        "X-CSRFToken": getCSRFToken(),
                    },
                });
        
                if (response.ok) {
                    updateProducts();
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

addToCart();


function deleteProduct() {
    const buttons = document.querySelectorAll(".overlay-button");
    buttons.forEach(function(button) {
        button.addEventListener("click", async function () {

            const productId = button.getAttribute("data-product-id");

            try {
                const response = await fetch(`/wishlist/delete/${productId}/`, { 
                    method: "DELETE",
                    headers: {
                        "X-CSRFToken": getCSRFToken(),
                    }
                });

                if (response.ok) {
                    updateProducts();
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


async function sendRequest(url) {
    try {
        const response = await fetch(url.toString());

        if (response.ok) {
            const html = await response.text();

            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const wishlistContainer  = doc.querySelector("#update-wishlist");
            document.querySelector("#update-wishlist").innerHTML = wishlistContainer .innerHTML;

            deleteProduct();
            updateSort();
            updateView();
            addToCart();
        
            history.replaceState(null, "", url.toString());
        } else {
            const error = await response.json();
            console.error(`Ошибка: ${error.message}`);
        }
    } catch (err) {
        console.error("Ошибка при загрузке данных:", err);
    }
};


async function updateProducts() {
    try {
        const urlParams = new URLSearchParams(window.location.search);
        const sortOrder = urlParams.get("sort") || '';
        const viewType = urlParams.get("view") || '';

        let fetchUrl;

        if (sortOrder !== '' && viewType === '') fetchUrl = `/wishlist/?sort=${sortOrder}`
        else if (sortOrder === '' && viewType !== '') fetchUrl = `/wishlist/?view=${viewType}`
        else if (sortOrder === '' && viewType === '') fetchUrl = '/wishlist/'
        else fetchUrl = `/wishlist/?sort=${sortOrder}&view=${viewType}`;

        const response = await fetch(fetchUrl);
        if (response.ok) {
            const html = await response.text();

            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const wishlistContainer = doc.querySelector("#update-wishlist");
            document.querySelector("#update-wishlist").innerHTML = wishlistContainer.innerHTML;

            deleteProduct();
            updateSort();
            updateView();
            addToCart();
        }
    } catch (err) { 
        console.error("Ошибка при обновлении:", err);
    }
};