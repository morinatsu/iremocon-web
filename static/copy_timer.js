// copy_timer.js
$(function(){
    $('input[name="copy_timer"]').on("click", function(){
	var date_time = new String($(this).parent().siblings('td.time').text());
	var date = date_time.substr(0, 10);
	var hour = date_time.substr(11, 2);
	var minute = date_time.substr(14, 2);
	var code = new String($(this).parent().siblings('td.code').text());
        $('#timer_form > p > select[name="date"]').val(date);
        $('#timer_form > p > select[name="hour"]').val(hour);
        $('#timer_form > p > select[name="minute"]').val(minute);
        $('#timer_form > p > select[name="Button"]').children().each(function (){
	    if ($(this).text() == code){
		var code_val = $(this).val();
                $('#timer_form > p > select[name="Button"]').val(code_val);
	    };
	});
    });
});
