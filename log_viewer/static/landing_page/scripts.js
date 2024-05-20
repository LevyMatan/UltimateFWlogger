document.getElementById('configureDeviceButton').addEventListener('click', function() {
    document.getElementById('configureDeviceForm').style.display = 'block';
});

document.getElementById('configureDeviceForm').addEventListener('submit', function(event) {
    event.preventDefault();
    document.getElementById('configureDeviceForm').style.display = 'none';
});