if (typeof jQuery === 'undefined') { throw new Error('requires jQuery') }

$(document).ready(function() {
	load_all_note();
});

function load_all_note() {
	$.getJSON("/i/loadall", function(data) {
		$.each(data, function(key, value) {
			var nc = value.length;
			var array = [];
			for (i = 0; i < value.length; i++) {
				var v = value[i];
				array.push('<p>');
				array.push('<input type="checkbox"' + (v.c == 1 ? "checked" : "") + '/>');
				array.push(v.t);
				array.push('</p>');
				nc -= v.c;
			}
			$("#" + key + "-div").html(array.join(''));
			$("#" + key + "-div").parent().find('.badge').html(nc + "");
		});
	});
}