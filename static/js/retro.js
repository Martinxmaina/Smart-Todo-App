// Add retro-style animations and effects
document.addEventListener('DOMContentLoaded', () => {
    // Add hover effect to task cards
    const taskCards = document.querySelectorAll('.task-card');
    taskCards.forEach(card => {
        card.addEventListener('mouseover', () => {
            card.style.transform = 'translateY(-5px)';
            card.style.boxShadow = '0 5px 15px rgba(0, 255, 255, 0.3)';
        });
        
        card.addEventListener('mouseout', () => {
            card.style.transform = 'translateY(0)';
            card.style.boxShadow = 'none';
        });
    });
    
    // Add click effect to buttons
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('div');
            ripple.classList.add('ripple');
            this.appendChild(ripple);
            
            const rect = button.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            
            setTimeout(() => ripple.remove(), 1000);
        });
    });
    
    // Add scanline effect
    const scanline = document.createElement('div');
    scanline.classList.add('scanline');
    document.body.appendChild(scanline);
    
    // Add glitch effect to title
    const title = document.querySelector('.glitch');
    if (title) {
        setInterval(() => {
            title.style.textShadow = `${Math.random() * 10 - 5}px ${Math.random() * 10 - 5}px var(--secondary)`;
            setTimeout(() => {
                title.style.textShadow = '2px 2px var(--secondary)';
            }, 50);
        }, 3000);
    }
});