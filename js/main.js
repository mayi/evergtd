if (typeof jQuery === 'undefined') { throw new Error('requires jQuery') }

$(document).ready(function() {
	load_all_note();
	$(".task-update").click(function() {
		update_note(this);
	});
});

function load_all_note() {
	$.getJSON("/i/loadall", function(data) {
		$.each(data, function(key, value) {
			load_note(key, value);
		});
	});
}

function load_note(name, value) {
	var nc = value.length;
	alert(nc);
	var array = [];
	for (i = 0; i < value.length; i++) {
		var v = value[i];
		array.push('<p>');
		array.push('<input type="checkbox"' + (v.c == 1 ? "checked" : "") + '/>');
		array.push(v.t);
		array.push('</p>');
		nc -= v.c;
	}
	$("#" + name + "-div").html(array.join(''));
	$("#" + name + "-badge").html(nc + "");
	alert(nc);
}

function update_note(obj) {
	var belong = $(obj).attr("belong");
	var array = [];
	$("#" + belong + "-div").children("p").each(function(i, item) {
		var c = $(item).find("input:checked").length;
		var t = $(item).text();
		array.push('{"c":' + c + ',"t":"' + t + '"}');
	});
	jsonString = '[' + array.join(',') + ']';
	$.post("/i/update", {"name": belong, "content": jsonString}, function(data) {
		alert(data);
		if (data.r == 0) {
			load_note(belong, $.parseJSON(data.data));
		}
	}, "json");
}