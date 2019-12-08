// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#dataTable_od').DataTable({
      order:[[1,"asc"]]
  });
});

$(document).ready(function() {
  $('#dataTable').DataTable({
      order:[[1,"asc"]]
  });
});
