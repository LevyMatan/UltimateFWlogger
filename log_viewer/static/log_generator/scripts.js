function uploadLogs() {
    var fileInput = document.getElementById('logFile');
    var filePath = fileInput.value;

    fetch('/upload_logs', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'filePath': filePath })
    }).then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    }).then(data => {
        console.log('File path sent successfully');
    }).catch(error => {
        console.error('Error:', error);
    });
}