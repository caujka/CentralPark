function switch_menu() { 
	var menu_bar = document.getElementsByClassName('top_menu_item')
	for(var i=0; i<menu_bar.length; i++){
		if('/' + menu_bar[i].id == document.location.pathname){
			menu_bar[i].classList.add('active');
	
		}
	}
}
