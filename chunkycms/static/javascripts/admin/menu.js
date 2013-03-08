$(document).ready(function() {
    $(".page-children").hide();

    $(".left-col a").click(function (event) {
	event.preventDefault();
	var target_link = $(this);
	var children_container = $(target_link.attr("href"));
	children_container.toggle(0, function() {
	    if (target_link.text() == "+") target_link.text("-");
	    else target_link.text("+");
	});
    });

    $(".left-col a").each(function () {
	var link = $(this);
	var children_container = $(link.attr("href"));

	if (children_container.find("li").length < 1) {
	    link.text("");
	}
    });
});
