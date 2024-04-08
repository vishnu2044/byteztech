document.getElementById('logout-button').addEventListener('click', function() {    
    console.log("its working::::::::") 
    localStorage.removeItem('token');
    window.location.href = '/signup';
  });

  var token = localStorage.getItem('token');

  $.ajax({
      url: 'profile',
      type: 'GET',
      headers: {
          'Authorization': 'Bearer ' + token
      },
      success: function(response) {
          console.log("user is authenticated")
          $('#profile-username').text(response.username);
          console.log(profile-username)
      },
      error: function(xhr, status, error) {
          console.log("Error", response.message)
      }
  });

  $.ajax({
    url: 'get-profile-details',
    type: 'GET',
    headers: {
        'Authorization': 'Bearer ' + token
    },
    success: function(response) {
        $('#profile-username').text(response.username);
        $('#profile-fullname').text(response.fullname);
        $('#profile-email').text(response.email);
    },
    error: function(xhr, status, error) {
        console.error("Error:", error);
    }
});

$.ajax({
  url: 'get_all_files',
  type: 'GET',
  headers: {
      'Authorization': 'Bearer ' + token
  },
  success: function(response) {
      console.log("Files data received successfully!");
      console.log(response);
      // Assuming response contains files_data
      for (let fileData of response.files_data) {
          // Create HTML elements and populate with file data
          const listItem = document.createElement('li');
          listItem.classList.add('list-group-item', 'my-2', 'text-dark', 'border-dark', 'rounded-3xl');
          listItem.innerHTML = `
              ${fileData.filename}
              <span class="float-right">
                  <span class="mr-3 text-dark">${fileData.file_type}</span>
                  <span class="mr-3 text-dark">${fileData.file_size} KB</span>
                  
              </span>`;
          document.querySelector('.list-group').appendChild(listItem);
      }
  },
  error: function(xhr, status, error) {
      console.error("Error:", error);
  }
});