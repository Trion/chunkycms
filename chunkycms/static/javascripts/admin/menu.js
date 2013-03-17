$(document).ready(function() {
    $(".children").hide();

    $(".left-col a").click(function (event) {
	event.preventDefault();
	var target_link = $(this);
	var children_container = $(target_link.attr("href"));
	children_container.toggle(0, function() {
	    var folder_icon = $("a.folder-icon[href="+ target_link.attr("href") + "]");
	    if (folder_icon.text() == "+") folder_icon.text("-");
	    else folder_icon.text("+");
	});
    });

    $(".left-col").each(function () {
	var left_col = $(this);
	var links = left_col.children();

	var folder_icon = $(links[0]);
	var title_link = $(links[1]);

	var children_container = $(title_link.attr("href"));

	if (children_container.find("li").length < 1) {
	    folder_icon.text("");
	    folder_icon.unbind("click").click(function (event) { event.preventDefault(); });
	    title_link.unbind("click").click(function (event) { event.preventDefault(); });
	}
    });
});
