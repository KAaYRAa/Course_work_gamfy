function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    
    if (sidebar) {
        sidebar.classList.toggle('active');
    
        if (sidebar.classList.contains('active')) {
            sidebar.style.transform = 'translateX(0)';
        } else {
            sidebar.style.transform = 'translateX(100%)';
        }
    } else {
        console.error("Елемент сайдбара з id='sidebar' не знайдено на сторінці!");
    }
}