console.log("hello");
const uploadForm = document.getElementById('upload-form');
const input = document.getElementById('id_file');
const token = localStorage.getItem('token');

const alertBox = document.getElementById('alert-box');
const progressBox = document.getElementById('progress-box');
const cancelBox = document.getElementById('cancel-box');
const cancelBtn = document.getElementById('cancel-btn');
const csrf = document.getElementsByName('csrfmiddlewaretoken');

input.addEventListener('change', () => {
    progressBox.classList.remove('not-visible');
    cancelBox.classList.remove('not-visible');

    const file_data = input.files[0];
    const fd = new FormData();
    fd.append('csrfmiddlewaretoken', csrf[0].value);
    fd.append('file', file_data);
    fd.append('token', token);

    $.ajax({
        type: 'POST',
        url: uploadForm.action,
        headers: {
            'Authorization': 'Bearer ' + token
        },
        data: fd,
        beforeSend: function(xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrf[0].value);
            xhr.setRequestHeader('Authorization', 'Token ' + token);
        },
        xhr: function() {
            const xhr = new window.XMLHttpRequest();
            xhr.upload.addEventListener('progress', e => {
                if (e.lengthComputable) {
                    const percent = e.loaded / e.total * 100;
                    progressBox.innerHTML = `<div class="progress">
                                                <div class="progress-bar" role="progressbar" style="width: ${percent}%" aria-valuenow="${percent}" aria-valuemin="0" aria-valuemax="100"></div>
                                            </div>
                                            <p>${percent.toFixed(1)}%</p>`;
                }
            });
            cancelBtn.addEventListener('click', () => {
                xhr.abort();
                progressBox.innerHTML = '';
                cancelBox.classList.add('not-visible');
            });
            return xhr;
        },
        success: function(response) {
            alertBox.innerHTML = `<div class="alert alert-success" role="alert">
                                        File uploaded successfully!
                                    </div>`;
            cancelBox.classList.add('not-visible');
            progressBox.classList.add('not-visible');
        },
        error: function(error) {
            console.log("Error response :: ", error);
        },
        cache: false,
        contentType: false,
        processData: false
    });
});
