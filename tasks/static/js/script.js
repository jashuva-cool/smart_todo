document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".list-group-item").forEach(item => {
        item.addEventListener("click", () => {
            item.style.transform = "scale(1.05)";
        });
    });
});