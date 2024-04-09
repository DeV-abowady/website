const xmlhttp = new XMLHttpRequest();

xmlhttp.onload = $(document).ready(function() {
    $('#table-data').html('');  // Clear existing table content
  
    $.ajax({
        url: '/get_table_data',
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            $.each(data, function(index, item) {
                var row = '<ul class="nav-list">' +
                            '<li class="nav-item">' + item.symbol + '</li>' +
                            '<li class="nav-item">' + item.price + '</li>' +
                            '<li class="nav-item">' + item.origQty + '</li>' +
                            '</ul>';
                $('#table-data').append(row);
            });
        }
    });
  });






