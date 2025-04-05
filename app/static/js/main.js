// Main JavaScript file for ScrumJET

// Initialize Alpine.js components when the script is loaded
document.addEventListener('alpine:init', () => {
    // Flash message component
    Alpine.data('flashMessages', () => ({
        messages: [],
        
        init() {
            // Get flash messages from the DOM
            const flashContainer = document.getElementById('flash-messages');
            if (flashContainer) {
                const messages = flashContainer.querySelectorAll('.alert');
                messages.forEach(message => {
                    this.messages.push({
                        category: message.dataset.category,
                        text: message.textContent.trim(),
                        visible: true
                    });
                });
            }
        },
        
        dismiss(index) {
            this.messages[index].visible = false;
        }
    }));
    
    // Mobile navigation component
    Alpine.data('mobileNav', () => ({
        open: false,
        
        toggle() {
            this.open = !this.open;
        },
        
        close() {
            this.open = false;
        }
    }));
    
    // Password strength component
    Alpine.data('passwordStrength', () => ({
        password: '',
        strength: 0,
        
        checkStrength() {
            let score = 0;
            
            // Length check
            if (this.password.length >= 8) score += 1;
            if (this.password.length >= 12) score += 1;
            
            // Complexity checks
            if (/[A-Z]/.test(this.password)) score += 1;
            if (/[a-z]/.test(this.password)) score += 1;
            if (/[0-9]/.test(this.password)) score += 1;
            if (/[^A-Za-z0-9]/.test(this.password)) score += 1;
            
            this.strength = Math.min(5, score);
        },
        
        strengthClass() {
            if (this.strength <= 1) return 'bg-danger';
            if (this.strength <= 3) return 'bg-warning';
            return 'bg-success';
        },
        
        strengthText() {
            if (this.strength <= 1) return 'Weak';
            if (this.strength <= 3) return 'Moderate';
            return 'Strong';
        }
    }));
});

// Auto-dismiss flash messages after 5 seconds
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(alert => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});

// Initialize tooltips
document.addEventListener('DOMContentLoaded', () => {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Initialize popovers
document.addEventListener('DOMContentLoaded', () => {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});