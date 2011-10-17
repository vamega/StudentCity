// JavaScript Document
var modalWindow = {
	parent:"body",
	windowId:null,
	content:null,
	width:null,
	height:null,
	close:function()
	{
		$(".modal-window").remove();
		$(".modal-overlay").remove();
	},
	open:function()
	{
		var modal = "";
		modal += "<div class=\"modal-overlay\"></div>";
		modal += "<div id=\"" + this.windowId + "\" class=\"modal-window\" style=\"width:" + this.width + "px; height:" + this.height + "px; margin-top:-" + (this.height / 2) + "px; margin-left:-" + (this.width / 2) + "px;\">";
		modal += this.content;
		modal += "</div>";	

		$(this.parent).append(modal);

		$(".modal-window").append("<a class=\"close-window\">Close</a>");
		$(".close-window").click(function(){modalWindow.close();});
	}
};


var openMyModal = function(content)
{
	modalWindow.windowId = "myModal";
	modalWindow.width = 480;
	modalWindow.height = 405;
	modalWindow.content = content;
	modalWindow.open();
};