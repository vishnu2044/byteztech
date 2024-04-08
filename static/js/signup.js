$(document).ready(function() {
    $('#signup-form').submit(function(event) {
        console.log("Form submitted!");
        event.preventDefault();
        
        var username = $('#username').val();
        var first_name = $('#first_name').val();
        var email = $('#email').val();
        var phoneno = $('#phoneno').val();
        var password = $('#password').val();
        var confirm_pass = $('#confirm_pass').val();
        
        if (!phoneno || phoneno.trim() === '') {
            alert('Please enter a phone number.');
            return;
        }
        if (password !== confirm_pass) {
            alert('Password does not match.');
            return;
        }
        if (!username || username.trim() === '') {
            alert('Please enter a username.');
            return;
        }
        if (!email || email.trim() === ''){
            alert("Please enter your email");
            return;
        }
        if (!first_name || first_name.trim() === ''){
            alert("Please enter your first name");
            return;
        }


        var formData = $(this).serialize();
        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: formData,
            dataType: 'json',
            success: function(response) {
                console.log("Response:", response);
                alert(response.message);
                if (response.redirect) {
                    window.location.href = response.redirect;
                }
            },
            error: function(xhr, errmsg, err) {
                if (xhr.status === 400) {
                    var responseJson = xhr.responseJSON;
                    alert(responseJson.message);
                } else {
                    console.error(xhr.status + ": " + xhr.responseText);
                }
            }
        });
    });
});