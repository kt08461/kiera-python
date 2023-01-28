var arrLink=[
	["/crawler/",''],
	["/students/",''],
	["/cifar10/",''],
	["https://app.powerbi.com/view?r=eyJrIjoiYjUyODhmN2YtZjA5NC00NmQzLWJiMjgtYzJhZTlhYzE2NzgzIiwidCI6IjllYTVjOTJkLTNiMDUtNGFkMy1iNjNiLTgzYjg2YjdmMzUyOSIsImMiOjEwfQ%3D%3D","_blank"],
	["https://app.powerbi.com/view?r=eyJrIjoiZmU4OTkxOWEtNjg0MS00ZGEwLThjZmEtZGM3NTZlZGIxYjdkIiwidCI6IjY4NThiMWYyLWI5YjQtNDk0Zi1iZWIxLTJmMjdlZDBkNDk1ZiIsImMiOjEwfQ%3D%3D","_blank"],
	["/cifar10_heroku/",'']
];

$(function () {
	$(".sidenav>a").click(function (e) {
		$(".sidenav>a.selected").removeClass();
		$(".content").html("<img src='/static/img/loading.gif'>");

		arr=arrLink[ $(this).addClass("selected").attr("id") ]
		if (arr[1] == "") {
			$(".content").load(arr[0]);
			e.preventDefault();
		} else {
			window.open(arr[0])
    		$(".content").html('');
		}
	}).first().click();
});

var pageChange=function(){
	var url = arrLink[0][0]+$('#page').val()+'/';

	$(".content").html("<img src='/static/img/loading.gif'>");
	$(".content").load(url);
}
