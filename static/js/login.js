var token = localStorage.getItem('token');
if (token) {
    console.log("token is present")
    window.location.href = '/profile';
}

document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();

    var email = $('#email').val();
    var password = $('#password').val();

    if (!email || email.trim() === '') {
        alert('Please enter an email.');
        return;
    }

    if (!password || password.trim() === '') {
        alert('Please enter a password.');
        return;
    }

    var formData = new FormData(this);
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/');
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    
    xhr.onload = function() {
        if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            if (response.token) {
                localStorage.setItem('token', response.token);
                window.location.href = '/profile';
            } else {
                alert('Token not found in response');
            }
        } else if (xhr.status === 401) {
            var errorResponse = JSON.parse(xhr.responseText);
            if (errorResponse.message) {
                alert(errorResponse.message);
            } else {
                alert('User not authencate Try again');
            }
        } else {
            alert('User not authencate Try again');
        }
    };

    xhr.send(formData);
});
