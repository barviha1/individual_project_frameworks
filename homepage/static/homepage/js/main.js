// Подставляет текущий год в подвал страницы.
const yearElement = document.getElementById("current-year");
if (yearElement) {
    yearElement.textContent = new Date().getFullYear();
}
