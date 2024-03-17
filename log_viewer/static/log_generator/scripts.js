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