document.addEventListener('DOMContentLoaded', () => {
    // Get all notifications
    const notifications = document.querySelectorAll('.notification');
    
    // Add click event to close buttons
    const closeButtons = document.querySelectorAll('.close-notification');
    closeButtons.forEach(button => {
        button.addEventListener('click', () => {
            const notification = button.parentElement;
            notification.style.opacity = '0';
            setTimeout(() => {
                notification.style.display = 'none';
            }, 300);
        });
    });
    
    // Auto-hide notifications after 5 seconds
    notifications.forEach(notification => {
        setTimeout(() => {
            notification.style.opacity = '0';
            setTimeout(() => {
                notification.style.display = 'none';
            }, 300);
        }, 5000);
    });
});