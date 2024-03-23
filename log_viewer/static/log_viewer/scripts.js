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
});