function handleDrop(event) {
    event.preventDefault();
    var files = event.dataTransfer.files;
    document.getElementById('file-upload').files = files;
    document.getElementById('file-upload').parentNode.submit();
}

function onFileChanged(event) {
    event.preventDefault();
    var files = event.target.files;
    document.getElementById('file-upload').files = files;
    document.getElementById('upload-form').submit();
}

document.getElementById('drop-area').addEventListener('dragenter', function (event) {
    this.classList.add('highlight');
});

document.getElementById('drop-area').addEventListener('dragleave', function (event) {
    this.classList.remove('highlight');
});

document.addEventListener('DOMContentLoaded', function () {
    fetch('/get_files')
        .then(response => response.json())
        .then(data => {
            const fileList = document.getElementById('file-list');
            data.files.forEach(file => {
                const li = document.createElement('li');
                li.textContent = file;
                fileList.appendChild(li);
            });
        })
        .catch(error => console.error('Error fetching files:', error));
});

document.getElementById('generate-rules').addEventListener('click', function (e) {
    e.preventDefault();

    document.getElementById('throbber').style.display = 'inline';

    fetch('/generate_rules')
        .then(response => response.json())
        .then(data => {
            if (data.message === 'success') {
                document.getElementById('throbber').style.display = 'none';
                document.getElementById('download-rules').style.display = 'inline-block';
                document.getElementById('view-ai-log').style.display = 'inline-block';
            }
        })
        .catch(error => console.error('Error: ', error));
});
