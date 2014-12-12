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
$('#rebels a').click(function (e) {
    e.preventDefault()
    $(this).tab('show')
    $("#bpc").hide();
    $("#relc").hide();
    $("#vot").hide();
    $("#rsc").show();
});
$('#votes a').click(function (e) {
    e.preventDefault()
    $(this).tab('show')
    $("#rsc").hide();
    $("#relc").hide();
    $("#bpc").hide();
    $("#vot").show();
});
$('#byparty a').click(function (e) {
    e.preventDefault()
    $(this).tab('show')
    $("#rsc").hide();
    $("#relc").hide();
    $("#vot").hide();
    $("#bpc").show();
});
$('#related a').click(function (e) {
    e.preventDefault()
    $(this).tab('show')
    $("#rsc").hide();
    $("#bpc").hide();
    $("#vot").hide();
    $("#relc").show();
});

jQuery('ul.nav li.dropdown').hover(function() {
  jQuery(this).find('.dropdown-menu').stop(true, true).delay(200).fadeIn();
}, function() {
  jQuery(this).find('.dropdown-menu').stop(true, true).delay(200).fadeOut();
});
$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})