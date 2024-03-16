$(document).ready(function () {
    var columNames = ['timestamp', 'file', 'src_function_name', 'level', 'msg']

    var table = $('#logTable').DataTable({
        "pageLength": 25,
        "autoWidth": false,
        "stripeClasses": ['odd-row', 'even-row'],
        "columnDefs": [
            { "orderable": false, "targets": [1, 2, 3, 4] } // Disables sorting on the 2nd, 3rd and 5th columns (0-indexed)
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
});