document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const mainNav = document.querySelector('.main-nav');
    const servicesDropdown = document.querySelector('.services-dropdown');
    const dropdownSpan = servicesDropdown?.querySelector('span');

    // Toggle mobile menu
    if (mobileMenuToggle && mainNav) {
        mobileMenuToggle.addEventListener('click', function() {
            this.classList.toggle('active');
            mainNav.classList.toggle('active');
            
            // Toggle aria-expanded
            const isExpanded = mainNav.classList.contains('active');
            this.setAttribute('aria-expanded', isExpanded);
            
            // Toggle body scroll
            const navLinks = mainNav.querySelector('.nav-links');
            if (navLinks) {
                navLinks.style.display = isExpanded ? 'flex' : 'none';
            }
        });
    }

    // Handle services dropdown on mobile
    if (dropdownSpan) {
        dropdownSpan.addEventListener('click', function(e) {
            if (window.innerWidth <= 768) {
                e.preventDefault();
                servicesDropdown.classList.toggle('active');
            }
        });
    }

    // Close mobile menu when clicking outside
    document.addEventListener('click', function(e) {
        if (window.innerWidth <= 768) {
            const isClickInsideNav = mainNav?.contains(e.target);
            const isClickOnToggle = mobileMenuToggle?.contains(e.target);
            
            if (!isClickInsideNav && !isClickOnToggle && mainNav?.classList.contains('active')) {
                mainNav.classList.remove('active');
                mobileMenuToggle?.classList.remove('active');
                mobileMenuToggle?.setAttribute('aria-expanded', 'false');
                document.body.style.overflow = '';
            }
        }
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
        if (window.innerWidth <= 768) {
            const isClickInsideDropdown = servicesDropdown?.contains(e.target);
            
            if (!isClickInsideDropdown) {
                servicesDropdown?.classList.remove('active');
            }
        }
    });

    // Handle window resize
    let resizeTimer;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function() {
            if (window.innerWidth > 768) {
                // Reset mobile menu state
                mainNav?.classList.remove('active');
                mobileMenuToggle?.classList.remove('active');
                mobileMenuToggle?.setAttribute('aria-expanded', 'false');
                servicesDropdown?.classList.remove('active');
                document.body.style.overflow = '';
            }
        }, 250);
    });

    // Close menu when clicking a link
    mainNav?.addEventListener('click', function(e) {
        if (window.innerWidth <= 768 && e.target.tagName === 'A') {
            mainNav.classList.remove('active');
            mobileMenuToggle?.classList.remove('active');
            mobileMenuToggle?.setAttribute('aria-expanded', 'false');
            document.body.style.overflow = '';
        }
    });
});
// Handle session cleanup when the page is unloaded
window.addEventListener('beforeunload', function() {
    // Send logout request to clean up server-side session
    fetch('/admin/logout', {
        method: 'POST',
        credentials: 'include'
    });
});
