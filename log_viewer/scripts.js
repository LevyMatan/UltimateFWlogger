document.addEventListener('DOMContentLoaded', function() {
    const logBody = document.getElementById('log-body');
    const searchInput = document.getElementById('search-input');
    const filterButton = document.getElementById('filter-button');

    // Dummy data for demonstration
    const logs = [
        { timestamp: '2024-03-08T10:00:00', level: 'INFO', message: 'Application started.' },
        { timestamp: '2024-03-08T10:05:00', level: 'DEBUG', message: 'Processing request...' },
        // Add more log entries here
    ];

    // Function to display log entries
    function displayLogs(logs) {
        logBody.innerHTML = ''; // Clear existing log entries
        logs.forEach(log => {
            const logRow = document.createElement('tr');
            logRow.innerHTML = `
                <td>${log.timestamp}</td>
                <td>${log.level}</td>
                <td>${log.message}</td>
            `;
            logBody.appendChild(logRow);
        });
    }

    // Initial display of logs
    displayLogs(logs);

    // Event listener for filter button
    filterButton.addEventListener('click', function() {
        const searchTerm = searchInput.value.toLowerCase();
        const filteredLogs = logs.filter(log =>
            log.message.toLowerCase().includes(searchTerm)
        );
        displayLogs(filteredLogs);
    });
});
