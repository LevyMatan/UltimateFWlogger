function generateLogs(num_of_logs, max_delay_ms) {
    fetch(`/sample_log_gen?num_of_logs=${num_of_logs}&max_delay_ms=${max_delay_ms}`, {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch((error) => {
        console.error('Error:', error);
    });
}

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