/**
 * Adds a click event listener to the "configureDeviceButton" element.
 * When the button is clicked, it displays the "configureDeviceForm" element.
 */
document.getElementById('configureDeviceButton').addEventListener('click', function() {
  document.getElementById('configureDeviceForm').style.display = 'block';
});

/**
 * Adds a submit event listener to the "configureDeviceForm" element.
 * When the form is submitted, it hides the "configureDeviceForm" element.
 */
document.getElementById('configureDeviceForm').addEventListener('submit', () => {
  document.getElementById('configureDeviceForm').style.display = 'none';
});
