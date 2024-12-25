document.addEventListener('DOMContentLoaded', function() {
    // Contact Form Validation and Submission
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
            }
        });
    }

    // Job Application Form Validation and Submission
    const applicationForm = document.getElementById('applicationForm');
    if (applicationForm) {
        applicationForm.addEventListener('submit', function(e) {
            if (!validateApplicationForm(this)) {
                e.preventDefault();
            }
        });
    }
});

// Form Validation Functions
function validateForm(form) {
    let isValid = true;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    // Clear previous error messages
    clearErrors(form);

    // Validate Name
    const nameInput = form.querySelector('#name');
    if (nameInput && nameInput.value.trim().length < 2) {
        showError(nameInput, 'Name must be at least 2 characters long');
        isValid = false;
    }

    // Validate Email
    const emailInput = form.querySelector('#email');
    if (emailInput && !emailRegex.test(emailInput.value)) {
        showError(emailInput, 'Please enter a valid email address');
        isValid = false;
    }

    // Validate Message
    const messageInput = form.querySelector('#message');
    if (messageInput && messageInput.value.trim().length < 10) {
        showError(messageInput, 'Message must be at least 10 characters long');
        isValid = false;
    }

    return isValid;
}

function validateApplicationForm(form) {
    let isValid = true;
    clearErrors(form);

    // Required fields validation
    const requiredFields = [
        { id: 'fullName', message: 'Please enter your full name' },
        { id: 'email', message: 'Please enter a valid email address' },
        { id: 'phone', message: 'Please enter your phone number' },
        { id: 'experience', message: 'Please enter your years of experience' },
        { id: 'coverLetter', message: 'Please provide a cover letter' }
    ];

    requiredFields.forEach(field => {
        const input = form.querySelector(`#${field.id}`);
        if (!input || !input.value.trim()) {
            showError(input, field.message);
            isValid = false;
        }
    });

    // Additional specific validations
    const emailInput = form.querySelector('#email');
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (emailInput && !emailRegex.test(emailInput.value)) {
        showError(emailInput, 'Please enter a valid email address');
        isValid = false;
    }

    const phoneInput = form.querySelector('#phone');
    const phoneRegex = /^\+?[\d\s-]{10,}$/;
    if (phoneInput && !phoneRegex.test(phoneInput.value)) {
        showError(phoneInput, 'Please enter a valid phone number');
        isValid = false;
    }

    const experienceInput = form.querySelector('#experience');
    if (experienceInput) {
        const experience = parseFloat(experienceInput.value);
        if (isNaN(experience) || experience < 0) {
            showError(experienceInput, 'Please enter a valid number of years');
            isValid = false;
        }
    }

    const coverLetterInput = form.querySelector('#coverLetter');
    if (coverLetterInput && coverLetterInput.value.trim().length < 100) {
        showError(coverLetterInput, 'Cover letter must be at least 100 characters long');
        isValid = false;
    }

    return isValid;
}

// Helper Functions
function showError(input, message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    input.classList.add('error');
    input.parentNode.insertBefore(errorDiv, input.nextSibling);
}

function clearErrors(form) {
    // Remove all error messages
    const errorMessages = form.querySelectorAll('.error-message');
    errorMessages.forEach(error => error.remove());

    // Remove error class from inputs
    const errorInputs = form.querySelectorAll('.error');
    errorInputs.forEach(input => input.classList.remove('error'));
}

// Optional: File Upload Validation
function validateFileUpload(input) {
    const maxSize = 5 * 1024 * 1024; // 5MB
    const allowedTypes = ['application/pdf', 'application/msword', 
                         'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];

    if (input.files.length > 0) {
        const file = input.files[0];
        
        if (file.size > maxSize) {
            showError(input, 'File size must be less than 5MB');
            return false;
        }
        
        if (!allowedTypes.includes(file.type)) {
            showError(input, 'Only PDF and Word documents are allowed');
            return false;
        }
    }
    return true;
}