const items = document.querySelectorAll(".item");
const dots = document.querySelectorAll(".dot");
const counter = document.getElementById("counter");

let currentIndex = 0;
let autoplayInterval;

function updateCarousel(index) {
    items.forEach((item, i) => {
        item.classList.remove("active");
        dots[i].classList.remove("active");
    });

    items[index].classList.add("active");
    dots[index].classList.add("active");
    counter.textContent = (index + 1).toString().padStart(2, "0");

    currentIndex = index;
}

function nextSlide() {
    const nextIndex = (currentIndex + 1) % items.length;
    updateCarousel(nextIndex);
}

function prevSlide() {
    const prevIndex = (currentIndex - 1 + items.length) % items.length;
    updateCarousel(prevIndex);
}

function startAutoplay() {
    autoplayInterval = setInterval(nextSlide, 5000);
}

function resetAutoplay() {
    clearInterval(autoplayInterval);
    startAutoplay();
}

// Botões
document.getElementById("next").addEventListener("click", () => {
    nextSlide();
    resetAutoplay();
});

document.getElementById("prev").addEventListener("click", () => {
    prevSlide();
    resetAutoplay();
});

// Dots
dots.forEach((dot, index) => {
    dot.addEventListener("click", () => {
        updateCarousel(index);
        resetAutoplay();
    });
});

// Iniciar autoplay ao carregar
startAutoplay();
