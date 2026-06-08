// Auto-hide flash messages after 4 seconds
document.addEventListener("DOMContentLoaded", function () {
    const flashes = document.querySelectorAll(".flash");
    flashes.forEach(function (flash) {
        setTimeout(function () {
            flash.style.opacity = "0";
            flash.style.transition = "opacity 0.4s ease";
            setTimeout(function () {
                flash.remove();
            }, 400);
        }, 4000);
    });
});
