$(function() {
    $('tr').each(function(i) {
        $( this ).delay(i*50).fadeIn(150);
    });
});

function showPopup(event, idx) {
    var em = $('#em1_' + idx).val() + '@' + $('#em2_' + idx).val();
    $('#link').html(em);
    $('#link').attr('href', 'mailto:' + em);
    
    if ($('#showPhoto').length > 0)
        $('#showPhoto').attr('src', '/media/' + $('#img_' + idx).val());
    $('#showName').html($('#name_' + idx).html());
    
    if ($('#showPosition').length > 0)
        $('#showPosition').html($('#position_' + idx).html());
    positionPopup(event, $('#emailPopup'));
    $('#closePopup').off().on('click', hidePopup);

    if ($('#showPhoto').length > 0)
        $(".profile_photo").on('mouseover', function(event) {
            $('#profilePhoto').attr('src', $('#showPhoto').attr('src'));
            positionPopup(event, $('#photoPopup'), true);
	    $('.popup-close').off().on('click', hidePopup);
        });
}
function hidePopup() {
    $('.popup').hide();
    $('.big_photo').hide();
}
