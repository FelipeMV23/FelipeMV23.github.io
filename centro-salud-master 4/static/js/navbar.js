document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.querySelector('#navbarToggle');
    const navbarMenu = document.querySelector('#navbarNav');

    menuToggle.addEventListener('click', function() {
        navbarMenu.classList.toggle('show');
    });

    document.addEventListener('click', function(event) {
        if (!navbarMenu.contains(event.target) && !menuToggle.contains(event.target)) {
            navbarMenu.classList.remove('show');
        }
    });
});
