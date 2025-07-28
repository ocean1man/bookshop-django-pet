document.addEventListener('DOMContentLoaded', function () {
    const slider = document.querySelector('.products__inner_flex');
    const prevBtn = document.querySelectorAll('.products__pagination-button-select')[0];
    const nextBtn = document.querySelectorAll('.products__pagination-button-select')[1];
    const products = document.querySelectorAll('.product');
    
    const productWidth = products[0].offsetWidth + 20;
    const visibleCount = getVisibleCount();
    const totalItems = products.length;

    let currentOffset = 0;

    function getVisibleCount() {
        if (window.innerWidth <= 576) return 1
        else if (window.innerWidth <= 1024) return 3
        else return 4;
    }

    function cloneProducts() {
        const fragment = document.createDocumentFragment();
        products.forEach(product => {
            const clone = product.cloneNode(true);
            fragment.appendChild(clone);
        });
        slider.appendChild(fragment);
    }

    cloneProducts();

    function updateSliderPosition() {
        slider.style.transition = 'transform 0.5s ease';
        slider.style.transform = `translateX(-${currentOffset}px)`;
    }

    function jumpWithoutTransition(offset) {
        slider.style.transition = 'none';
        slider.style.transform = `translateX(-${offset}px)`;
    }

    nextBtn.addEventListener('click', () => {
        const maxOffset = productWidth * totalItems;
        currentOffset += productWidth * visibleCount;

        updateSliderPosition();

        if (currentOffset >= maxOffset) {
            setTimeout(() => {
                currentOffset = 0;
                jumpWithoutTransition(currentOffset);
            }, 500);
        }
    });

    prevBtn.addEventListener('click', () => {
        const maxOffset = productWidth * totalItems;
    
        if (currentOffset === 0) {
            currentOffset = maxOffset;
            jumpWithoutTransition(currentOffset);
    
            setTimeout(() => {
                currentOffset -= productWidth * visibleCount;
                updateSliderPosition();
            }, 20);
        } else {
            currentOffset -= productWidth * visibleCount;
            updateSliderPosition();
        }
    });
});

const slider = document.querySelector('.best-slider');
slider.innerHTML += slider.innerHTML;

if (window.innerWidth <= 576) {
    let firstSection = document.querySelector('.section__container');
    firstSection.classList.add('section__container_extended');

    let lastSection = document.querySelectorAll('.section__container')[4];
    lastSection.classList.add('section__container_extended');
    lastSection.style.display = 'block';
}