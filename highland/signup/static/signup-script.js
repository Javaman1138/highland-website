$(function() {
	$('#signup_button').on('click', function() {
	    $('#error_list').empty();
		form = $('#request_signup_form');
		$('#id_name').removeClass('error_field');
		$('#id_email').removeClass('error_field');
		$.ajax({
			url : form.attr('action'),
			type : form.attr('method'),
			dataType: 'json',
			data : form.serialize(),
			success : successHandler,
			error : errorHandler
		});
	});
});

function successHandler(data) {
    if (data.success == false) {
    	if (data.errors) {
    	    err_list = $('#error_list')
    	    err_list.append('<li>Please correct the highlighted fields</li>');

    		$.each(data.errors, function(field_name, error_msg) {
    		    $('#id_' + field_name).addClass('error_field');
    		});
    		$('#error_div').show();
    	} else if (data.error) {
	    alert(data.error);
	}
    } else {
    	$('#input_div').hide();
        $('#email_addr').html(data.email_addr);
    	$('#our_addr').html(data.our_addr);
    	$('#success_div').show();
	if (typeof autoResetInterval !== 'undefined') {
		console.debug('interval=' + autoResetInterval);
		setTimeout(resetForm, autoResetInterval);
	}
    }
}

function errorHandler(xhr, err) {
    alert ('Houston, we have a problem! ' + err);
}
function resetForm() {
	console.debug('reset...');
	if ($('#success_div').is(":visible")) {
		$('#id_name').val('')
		$('#id_email').val('')
    		$('#success_div').hide();
	    	$('#input_div').show();
	}
}
