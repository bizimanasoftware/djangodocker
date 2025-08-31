document.addEventListener('DOMContentLoaded', function () {
    const donationForm = document.getElementById('donation-form');
    if (!donationForm) return;

    const formMessage = document.getElementById('form-message');
    const progressBar = document.getElementById('progress-bar');
    const progressText = document.getElementById('progress-text');
    const currentAmountText = document.getElementById('current-amount');
    const csrfToken = donationForm.querySelector('[name=csrfmiddlewaretoken]').value;

    donationForm.addEventListener('submit', function (e) {
        e.preventDefault(); // Prevent the default page reload

        const formData = new FormData(donationForm);
        const actionUrl = donationForm.getAttribute('action');
        
        // Show a loading state
        formMessage.className = 'alert alert-info';
        formMessage.textContent = 'Processing your donation...';

        fetch(actionUrl, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest', // Important for Django to identify it as an AJAX request
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // --- UPDATE UI ON SUCCESS ---
                formMessage.className = 'alert alert-success';
                formMessage.textContent = data.message;
                
                // Update the progress bar
                const newProgress = parseFloat(data.new_progress).toFixed(2);
                progressBar.style.width = newProgress + '%';
                progressBar.setAttribute('aria-valuenow', newProgress);
                progressText.textContent = newProgress + '%';
                
                // Update the 'Raised' amount
                currentAmountText.textContent = data.new_total;
                
                // Clear the input field
                document.getElementById('donation-amount').value = '';

            } else {
                // --- SHOW ERROR MESSAGE ---
                formMessage.className = 'alert alert-danger';
                formMessage.textContent = data.message || 'An error occurred.';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            formMessage.className = 'alert alert-danger';
            formMessage.textContent = 'A network error occurred. Please check your connection and try again.';
        });
    });
});
