$(document).ready(function() {
  var table = $('#logTable').DataTable({
    pageLength: 1000,
    autoWidth: false,
    scrollY: '97%',
    scrollCollapse: false,
    stripeClasses: ['odd-row', 'even-row'],
    deferRender: true,
    scroller: true,
    select: true,
    columns: [
      {data: 'timestamp', searchPanes: {show: false}},
      {data: 'file_line', searchPanes: {show: false}},
      {data: 'src_function_name', searchPanes: {show: true}},
      {data: 'level', searchPanes: {show: true}}, {data: 'log_group', searchPanes: {show: true}},
      {data: 'msg', searchPanes: {show: false}}
    ],
    columnDefs: [
      {
        targets: '_all',
        orderable: false,
      },
      {targets: 5, className: 'search-hilite'}
    ],
    dom: 'Plfrtip',  // P is for searchPanes
    searchPanes: {
      cascadePanes: true,   // Initialize in a collapsed state
      layout: 'columns-3',  // Layout the panes in three columns
      viewTotal: true,      // Show the total number of records in the dataset
      initCollapsed: true   // Initialize in a collapsed state
    },
  });

  var selectedRowId;

  table.on('click', 'tr', function() {
    if ($(this).hasClass('selected')) {
      $(this).removeClass('selected');
      selectedRowId = null;
    } else {
      table.$('tr.selected').removeClass('selected');
      $(this).addClass('selected');
      selectedRowId = table.row(this).id();
    }
  });

  table.on('draw', function() {
    var body = $('.search-hilite', table.table().body());

    body.unhighlight();
    body.highlight(table.search());

    if (selectedRowId) {
      var row = table.row('#' + selectedRowId);
      if (row.length) {
        row.nodes().to$().addClass('selected');
      }
    }
  });

  setInterval(function() {
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
  }, 1500);

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

  // Add the updateLogGroupValue function as an event listener for the change event of the
  // checkboxes
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

  var lastFoundIndex = -1;
  var lastFoundText = '';

  function findAndScrollToRow(text, direction) {
    var foundIndex = -1;
    if (text !== lastFoundText) {
      lastFoundIndex = -1;
    }

    if (lastFoundIndex === -1) {
      // direction does not matter, set as next
      direction = 'next';
    }

    if (direction !== 'next' && direction !== 'back') {
      alert('Invalid direction.');
      return;
    }
    if (direction === 'next') {
      // Iterate through each row's data to find the text
      table.rows().every(function(rowIdx, tableLoop, rowLoop) {
        // Start searching from the next row after the last found index
        if (rowIdx <= lastFoundIndex) {
          foundIndex = -1;
          return;
        }
        var data = this.data();
        if (data && data['msg'].includes(text)) {
          foundIndex = rowIdx;
          return false;  // Break the loop once the text is found
        }
      });
    } else {
      var totalRows = table.rows().count();
      var start_from = totalRows;
      if (lastFoundIndex !== -1) {
        start_from = lastFoundIndex;
      }

      for (var i = start_from - 1; i >= 0; i--) {
        var row = table.row(i);
        if (row['msg'].includes(text)) {
          foundIndex = rowIdx;
          return false;  // Break the loop once the text is found
        }
      }
    }

    if (foundIndex !== -1) {
      // Update the last found index
      lastFoundIndex = foundIndex;
      console.log('Found at index:', foundIndex);
      // Scroll to the found row
      table.row(foundIndex).scrollTo();

      // Optionally, highlight the row
      $(table.row(foundIndex).node()).addClass('highlight');
    } else {
      alert('Text not found in the table.');
    }
  }

  $('#jumpToBackButton').on('click', function() {
    var searchText = $('#jumpTo').val();
    findAndScrollToRow(searchText, 'back');
  });
  $('#jumpToNextButton').on('click', function() {
    var searchText = $('#jumpTo').val();
    findAndScrollToRow(searchText, 'next');
  });
});