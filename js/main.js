if (typeof jQuery === 'undefined') { throw new Error('requires jQuery') }

$(document).ready(function() {
	load_all_note();
	$(".task-update").click(function() {
		update_note(this);
	});
	$(".task-add").click(function() {
		add(this);
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
	$.ajax({
		type: "POST",
		url: "/i/update",
		data: {name: belong, content: jsonString},
		dataType: "json"
	}).done(function(data) {
		if (data.r == 0) {
			load_note(belong, data.data);
		}
	});
}

function add(obj) {
	var belong = $(obj).attr("belong");
	$("#" + belong + "-div").append('<p><div class="input-group"><span class="input-group-addon"><input type="checkbox"></span><input type="text" class="form-control"><span class="input-group-btn"><button class="btn btn-default" type="button">Save</button></div></p>');
}