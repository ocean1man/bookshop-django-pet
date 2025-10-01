import { getCSRFToken } from './getCSRF.js';

function addToCart() {
    let addButtons = document.querySelectorAll(".action-button:not(.action-button_disabled):not(.action-button_active)");
    addButtons.forEach(button => {
        button.addEventListener("click", async function () {

            const productId = button.getAttribute("data-product-id"); 
    
            let url = new URL(window.location.href);
    
            try {
                const response = await fetch(`/cart/add/${productId}/`, { 
                    method: "POST",
                    headers: {
                        "X-CSRFToken": getCSRFToken(),
                    },
                });
    
                if (response.ok) {
                    sendRequest(url.toString());
                } else {
                    const error = await response.json();
                    console.error(`Ошибка: ${error.message}`);
                }
            } catch (err) {
                console.error("Ошибка добавления товара:", err);
            }
    });
})};

addToCart();


function editWishlist() {
    const button = document.querySelector('.overlay-button');
    button.addEventListener('click', async function() {

        const productId = button.getAttribute('data-product-id');
        let method;
        let requestUrl;

        let url = new URL(window.location.href);

        if (button.classList.contains("overlay-button_active")) {
            method = "DELETE";
            requestUrl = `/wishlist/delete/${productId}/`;
        } else {
            method = "POST";
            requestUrl = `/wishlist/add/${productId}/`;
        }

        try {
            const response = await fetch(requestUrl, { 
                method: method,
                headers: {
                    "X-CSRFToken": getCSRFToken(),
                }
            });
    
            if (response.ok) {
                sendRequest(url.toString());
            } else {
                const error = await response.json();
                console.error(`Ошибка: ${error.message}`);
            }
        } catch (err) {
            console.error("Ошибка добавления товара:", err);
        }
    });
};

editWishlist();

// OB - OverlayButton
function setDefaultOB() {
    if (window.innerWidth <= 768) {
        const overlayButton = document.querySelector('.overlay-button');

        overlayButton.classList.remove('overlay-button_large');
    
        const svg = overlayButton.querySelector('svg');
    
        const oldPath = svg.querySelector('path');
        oldPath.remove();
    
        const newPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        newPath.setAttribute('d', 'M13.5168 5.57998L12.6968 6.40198L11.8728 5.57798C10.8647 4.57003 9.49754 4.00382 8.07198 4.00391C6.64643 4.00401 5.27929 4.5704 4.27134 5.57848C3.26338 6.58657 2.69717 7.95378 2.69727 9.37934C2.69736 10.8049 3.26375 12.172 4.27184 13.18L12.1668 21.075C12.3075 21.2154 12.4981 21.2943 12.6968 21.2943C12.8956 21.2943 13.0862 21.2154 13.2268 21.075L21.1288 13.178C22.1357 12.1698 22.7012 10.8031 22.701 9.37828C22.7008 7.95341 22.135 6.58689 21.1278 5.57898C20.6282 5.07903 20.035 4.68242 19.382 4.41182C18.729 4.14123 18.0292 4.00195 17.3223 4.00195C16.6155 4.00195 15.9156 4.14123 15.2627 4.41182C14.6097 4.68242 14.0165 5.07903 13.5168 5.57898V5.57998ZM20.0648 12.12L12.6968 19.485L5.33184 12.12C4.96887 11.7609 4.68045 11.3335 4.48317 10.8626C4.28589 10.3916 4.18363 9.88632 4.18227 9.37572C4.18092 8.86511 4.28048 8.35927 4.47526 7.88727C4.67003 7.41527 4.95617 6.98642 5.31722 6.62537C5.67828 6.26431 6.10713 5.97818 6.57912 5.7834C7.05112 5.58863 7.55696 5.48906 8.06757 5.49042C8.57817 5.49178 9.08348 5.59404 9.55443 5.79132C10.0254 5.9886 10.4527 6.27702 10.8118 6.63998L12.1698 7.99698C12.2405 8.06772 12.3246 8.12362 12.4171 8.16139C12.5097 8.19915 12.6089 8.21804 12.7089 8.21692C12.8088 8.2158 12.9076 8.19471 12.9993 8.15487C13.091 8.11504 13.1738 8.05728 13.2428 7.98498L14.5768 6.63998C15.3121 5.95556 16.2842 5.583 17.2886 5.60067C18.293 5.61834 19.2514 6.02487 19.9622 6.73474C20.673 7.44461 21.0807 8.40249 21.0997 9.40686C21.1186 10.4112 20.7473 11.3838 20.0638 12.12H20.0648Z');
    
        svg.appendChild(newPath);
    }
}

setDefaultOB();


async function sendRequest(url) {
    try {
        const response = await fetch(url.toString());

        if (response.ok) {
            const html = await response.text();

            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const mainContainer = doc.querySelector(".main-product");
            document.querySelector(".main-product").innerHTML = mainContainer.innerHTML;

            editWishlist();
            addToCart();
            setDefaultOB();
        
        } else {
            const error = await response.json();
            console.error(`Ошибка: ${error.message}`);
        }
    } catch (err) {
        console.error("Ошибка при загрузке данных:", err);
    }
};