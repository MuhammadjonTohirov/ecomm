document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    // First, make a request to the JWT endpoint to get tokens
    fetch('/crm/api/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.data && data.data.access_token && data.data.refresh_token) {
            // Store tokens in localStorage
            localStorage.setItem('access_token', data.data.access_token);
            localStorage.setItem('refresh_token', data.data.refresh_token);
            
            if (data.data.expires_in) {
                localStorage.setItem('token_expiry', data.data.expires_in);
            }
            
            if (data.data.user) {
                localStorage.setItem('user_info', JSON.stringify(data.data.user));
            }
            
            // Then submit the form normally for session-based authentication
            const form = document.getElementById('loginForm');
            form.method = 'post';
            form.removeEventListener('submit', arguments.callee);
            form.submit();
        } else if (data.error) {
            // Show error message
            const errorElement = document.getElementById('loginError');
            errorElement.textContent = data.error;
            errorElement.classList.remove('d-none');
        }
    })
    .catch(error => {
        console.error('Login error:', error);
        const errorElement = document.getElementById('loginError');
        errorElement.textContent = 'An error occurred while trying to log in. Please try again.';
        errorElement.classList.remove('d-none');
    });
});
