$('#constituencies a').click(function (e) {
    e.preventDefault()
    $(this).tab('show')
    $("#rc").hide();
    $("#cc").show();
});
$('#regions a').click(function (e) {
    e.preventDefault()
    $(this).tab('show')
    $("#cc").hide();
    $("#rc").show();
});
$('#rebellions a').click(function (e) {
    e.preventDefault()
    $(this).tab('show')
    $("#attend").hide();
    $("#rebel").show();
});
$('#attendance a').click(function (e) {
    e.preventDefault()
    $(this).tab('show')
    $("#rebel").hide();
    $("#attend").show();
});