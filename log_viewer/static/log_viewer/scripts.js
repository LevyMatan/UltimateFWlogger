$(document).ready(function () {
    var columNames = ['timestamp', 'file', 'src_function_name', 'level', 'msg']

    var table = $('#logTable').DataTable({
        "pageLength": 1000,
        "autoWidth": false,
        "scrollY": "97%",
        "scrollCollapse": false,
        "stripeClasses": ['odd-row', 'even-row'],
        "ajax": "/latest_logs",
        "order": [[0, "desc"]],
        "columns": [
            { "data": "timestamp"},
            { "data": "file_line"},
            { "data": "src_function_name"},
            { "data": "level"},
            { "data": "msg"}
        ],
        "columnDefs": [
            { "orderable": false, "targets": [1, 2, 3, 4] }
        ],
    });

    // Initialize the autocomplete widgets
    $('.column-filter').each(function () {
        var column = table.column($(this).data('column'));
        var columnName = $(this).attr('data-name');

        $.getJSON('/unique/' + columnName, function(data) {
            $('#' + columnName + '-filter').autocomplete({
                source: data,
                select: function (event, ui) {
                    var result_set = column.search(ui.item.value);
                    column.search(ui.item.value).draw();
                    $.get('/logs/filters/' + columnName + '/' + ui.item.value);
                }
            });
        });
    });

    // Add click event handler for the filter button
    $('#apply-filter').click(function () {
        var filterValue = $('#msg-filter').val();
        table.column(4).search(filterValue).draw();
    });

    setInterval(function () {
        fetch('/latest_logs')
        .then(response => {
            if (!response.ok) {
                console.error('Error status:', response.status);
                return response.text().then(text => {
                    throw new Error('Error response: ' + text);
                });
            }
            return response.json();
        })
        .then(data => {
            table.rows.add(data.data).draw();
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }, 500);

    // Initialize the variable to hold the bitwise OR value
    var logGroupValue = 0;

    // Function to initialize the logGroupValue when the page is ready
    function initializeLogGroupValue() {
        // Get all the checkboxes
        var checkboxes = document.querySelectorAll('input[type="checkbox"]');

        // Iterate over the checkboxes
        for (var i = 0; i < checkboxes.length; i++) {
            // If the checkbox is checked, add its value to the logGroupValue
            if (checkboxes[i].checked) {
                logGroupValue |= parseInt(checkboxes[i].value);
            }
        }

        // Convert logGroupValue to an unsigned 32-bit integer
        logGroupValue >>>= 0;

        // Print the logGroupValue in binary format to the console
        // console.log(logGroupValue.toString(2));
    }

    // Function to update the logGroupValue when a checkbox is checked or unchecked
    function updateLogGroupValue(event) {
        // Get the checkbox that was changed
        var checkbox = event.target;

        // Get the value of the checkbox
        var value = parseInt(checkbox.value);
        // Print the logGroupValue in binary format to the console
        // console.log(value.toString(2));
        
        // If the checkbox is checked, do a bitwise OR operation with the value
        // If the checkbox is unchecked, do a bitwise AND operation with the bitwise NOT of the value
        // Convert logGroupValue to an unsigned 32-bit integer
        logGroupValue >>>= 0;
        turn_on_value = (logGroupValue | value)
        turn_on_value >>>= 0;
        // console.log(turn_on_value.toString(2));
        turn_off_value = (logGroupValue & ~value)
        turn_off_value >>>= 0;
        // console.log(turn_off_value.toString(2));
        logGroupValue = checkbox.checked ? turn_on_value : turn_off_value;
        
        console.log(logGroupValue.toString(2));
    }

    // Add the updateLogGroupValue function as an event listener for the change event of the checkboxes
    document.querySelectorAll('#sidebar input[type="checkbox"]').forEach(function(checkbox) {
        checkbox.addEventListener('change', updateLogGroupValue);
    });

    // Call the initializeLogGroupValue function once to initialize the logGroupValue
    initializeLogGroupValue();
    // Get the toggle checkbox
    var toggleAll = document.getElementById('toggleAll');

    // Add an event listener to the toggle checkbox
    toggleAll.addEventListener('change', function() {
        // Get all the checkboxes
        var checkboxes = document.querySelectorAll('input[type="checkbox"]');

        // Iterate over the checkboxes
        for (var i = 0; i < checkboxes.length; i++) {
            // If the toggle checkbox is checked, check the checkbox
            // If the toggle checkbox is unchecked, uncheck the checkbox
            checkboxes[i].checked = toggleAll.checked;
        }

        logGroupValue = toggleAll.checked ? 0xFFFFFFFF : 0;

    });
});