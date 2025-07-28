function updateSearch() {
    const form = document.querySelector('#search-form');
    form.addEventListener('submit', function(event) {

        event.preventDefault();

        const formData = new FormData(form);

        let url = new URL(window.location.href);

        formData.forEach((value, key) => {
            if (value === '') {
                url.searchParams.delete(key);
            } else {
                url.searchParams.set(key, value);
            }
        });

        url.searchParams.delete('page'); 
        url.searchParams.delete('author');
        url.searchParams.delete('age_limit');
        url.searchParams.delete('century_publication');
        url.searchParams.delete('min_price');
        url.searchParams.delete('max_price');
        url.searchParams.delete('genre'); 

        sendRequest(url)
    });
};

updateSearch();


async function updatePrice() {
    const form = document.querySelector('#price-form');
    form.addEventListener('submit', function(event) {

        event.preventDefault();

        const formData = new FormData(form);

        let url = new URL(window.location.href);

        formData.forEach((value, key) => {
            if (value === '') {
                url.searchParams.delete(key);
            } else {
                url.searchParams.set(key, value);
            }
        });

        url.searchParams.delete('page');

        sendRequest(url)
    });
};

updatePrice();


function updateCenturyPublications() {
    const radioButtons = document.querySelectorAll('input[name="century_publication"]');
    radioButtons.forEach(function(radio) {
        radio.addEventListener('change', function(event) {

            const form = document.getElementById('century-publication-form');

            let formData = new FormData(form);
            let century_publication = event.target.value;
            formData.set('century_publication', century_publication);

            let url = new URL(window.location.href);
            
            formData.forEach((value, key) => {
                url.searchParams.set(key, value);
            });

            url.searchParams.delete('page');

            sendRequest(url)
        });
    });
};

updateCenturyPublications();


function updateAuthors() {
    const radioButtons = document.querySelectorAll('input[name="author"]');
    radioButtons.forEach(function(radio) {
        radio.addEventListener('change', function(event) {

            const form = document.getElementById('author-form');

            let formData = new FormData(form);
            let author = event.target.value;
            formData.set('author', author);

            let url = new URL(window.location.href);
            
            formData.forEach((value, key) => {
                url.searchParams.set(key, value);
            });

            url.searchParams.delete('page');

            sendRequest(url)
        });
    });
};

updateAuthors();


function updateAgeLimits() {
    const radioButtons = document.querySelectorAll('input[name="age_limit"]');
    radioButtons.forEach(function(radio) {
        radio.addEventListener('change', function(event) {

            const form = document.getElementById('age-limit-form');

            let formData = new FormData(form);
            let age_limit = event.target.value;
            formData.set('age_limit', age_limit);

            let url = new URL(window.location.href);
            
            formData.forEach((value, key) => {
                url.searchParams.set(key, value);
            });

            url.searchParams.delete('page');

            sendRequest(url)
        });
    });
};

updateAgeLimits();


function updateGenres() {
    const checkboxes = document.querySelectorAll('input[name="genre"]');
    checkboxes.forEach(function(checkbox) {
        checkbox.addEventListener('change', function() {

            const form = document.getElementById('genre-form')

            let formData = new FormData(form);

            let url = new URL(window.location.href);

            formData.forEach((value, key) => {
                if (key === 'genre') {
                    if (form.querySelectorAll('input[name="genre"]:checked').length === 0) {
                        url.searchParams.delete(key);
                    } else {
                        url.searchParams.set(key, value);
                    }
                } else {
                    url.searchParams.set(key, value);
                }
            });

            // Удаление необходимо для предотвращения дублирования жанров
            url.searchParams.delete('genre');

            const selectedGenres = Array.from(form.querySelectorAll('input[name="genre"]:checked'))
                .map(checkbox => checkbox.value);

            selectedGenres.forEach(genre => {
                url.searchParams.append('genre', genre);
            });

            url.searchParams.delete('page');

            sendRequest(url)
        });
    });
};

updateGenres();


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
}

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


function goToPage() {
    const buttons = document.querySelectorAll('.products__pagination-button-select');
    buttons.forEach(function(button) {
        button.addEventListener('click', function() {

            let page = button.getAttribute('data-page');

            let url = new URL(window.location.href);
            url.searchParams.set('page', page);
        
            if (page === '1') url.searchParams.delete('page'); 
        
            sendRequest(url)

            window.scrollTo({
                top: 0,
                left: 0,
                behavior: "smooth"
            });
        });
    });
};

goToPage();


function showOrHideFilters() {
    const button = document.querySelector('.sort__show-hide-button');
    button.addEventListener('click', function() {
        const urlParams = new URLSearchParams(window.location.search);
        let url = new URL(window.location.href);
        let show = urlParams.get('show_filters') || '';
        if (show === '') {
            url.searchParams.set('show_filters', 'on');
            sendRequest(url)

        }
        else {
            url.searchParams.delete('show_filters')
            sendRequest(url)
        }
    })
}

showOrHideFilters();


function resetFilter() {
    const button = document.querySelector('.filter__clear-button');
    button.addEventListener('click', function() {

        const urlParams = new URLSearchParams(window.location.search);
        let query = urlParams.get('search') || '';
        let viewType = urlParams.get('view') || '';
        let sortOrder = urlParams.get('sort') || '';
    
        let url = new URL(window.location.href);
        if (query !== '') url.searchParams.set('search', query);
        if (viewType !== '') url.searchParams.set('view', viewType);
        if (sortOrder !== '') url.searchParams.set('sort', sortOrder);
    
        url.searchParams.delete('page'); 
        url.searchParams.delete('author');
        url.searchParams.delete('age_limit');
        url.searchParams.delete('century_publication');
        url.searchParams.delete('min_price');
        url.searchParams.delete('max_price');
        url.searchParams.delete('genre'); 
    
        sendRequest(url)

        window.scrollTo({
            top: 0,
            left: 0,
            behavior: "smooth"
        });
    });
}  

resetFilter();


function addToCart() {
    const buttons = document.querySelectorAll('#buy-button');
    buttons.forEach(function(button) {
        button.addEventListener('click', async function() {

            const productId = button.getAttribute('data-product-id');

            let url = new URL(window.location.href);

            try {
                const response = await fetch(`/cart/add/${productId}/`, { 
                    method: "POST",
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
    });
};

addToCart();


function editWishlist() {
    const buttons = document.querySelectorAll('.overlay-button');
    buttons.forEach(function(button) {
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
    });
};

editWishlist();


async function sendRequest(url) {
    try {
        const response = await fetch(url.toString());

        if (response.ok) {
            const html = await response.text();

            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const catalogContainer = doc.querySelector("#update-catalog");
            document.querySelector("#update-catalog").innerHTML = catalogContainer.innerHTML;

            updateSearch();
            updatePrice();
            updateCenturyPublications();
            updateAuthors();
            updateAgeLimits();
            updateGenres();
            updateSort();
            updateView();
            addToCart();
            editWishlist();
            goToPage();
            resetFilter();
            showOrHideFilters();
            setFilters();
        
            history.replaceState(null, "", url.toString());
        } else {
            const error = await response.json();
            console.error(`Ошибка: ${error.message}`);
        }
    } catch (err) {
        console.error("Ошибка при загрузке данных:", err);
    }
};


function getCSRFToken() {
    const cookieValue = document.cookie
      .split("; ")
      .find((row) => row.startsWith("csrftoken="))
      ?.split("=")[1] || "";
    return cookieValue;
};


function setFilters() {
    if (window.innerWidth > 576) {
        document.querySelector('.sort__filters').style.display = "block"
    };
}

setFilters();