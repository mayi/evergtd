if (typeof jQuery === 'undefined') { throw new Error('requires jQuery') }

$(document).ready(function() {

}

function load_all_note() {
	$.getJSON("/loadall", function(data) {
		
	});
}