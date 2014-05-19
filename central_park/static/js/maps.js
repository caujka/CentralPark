//ajax_return_data_parking(res)
var date1="";
function date1click(){
    date1=$("#data_id1").val();
    ajax_statistic_init_return(date1, $("#place_id").val());
    }

function ajax_statistic_init_return(date, parking_name)
{
$("#year_statistic_div").html("<marquee><h3>...loading...</h3><marquee>"); 
$("#day_statistic_div").html(""); 
$.ajax({
    url:"/statistic_ajax_year",
        data: {"parking_name":parking_name,
                "date1":date
        },
        contentType: 'application/json',
        success: function(res){
$("#year_statistic_div").html(""); 
$("#day_statistic_div").html(""); 
  drawYearStat(res["statistics_year"]);
  drawDayStat(res["statistics_day"]);   
}
      }); 

};

function initialize() {

function ajax_return_info(_marker,res)
{
  call_info_window(_marker,res["info"]);
  $("#place_id [value="+"'"+res['place_name']+"']").attr("selected", "selected");
//  drawChart(res["statistics"]);
//  drawBar();
}

function ajax_init_info(_marker,str)
{
$.ajax({
    url:"/maps_ajax_info",
        data: {"parking_name":str,
                "date1":date1,
                "date2":""
        },
        contentType: 'application/json',
        success: function(res){ajax_return_info(_marker,res);}
      }); 

};

  var myLatlng = new google.maps.LatLng(49.8392491,24.0300454);
  var mapOptions = {
    zoom: 12,
    center: myLatlng
  };

  var map = new google.maps.Map(document.getElementById('map-canvas'),
      mapOptions);
  var markers = [];  
function getRandom(min, max)
{
  return Math.random() * (max - min) + min;
}
  
var contentString = '';  
var infowindow = new google.maps.InfoWindow({
      content: contentString,
  });
  
//loading parking positions
function ajax_marker_add_response(res)
{
  for (var i =0; i<res['position'].length; i++){
  addMarker(new google.maps.LatLng(res['position'][i][0],res['position'][i][1]), res['position'][i][2]);
  }
};

function ajax_marker_add_request()
{
$.ajax({
    url:"/maps_ajax_marker_add",
        data: {"marker":"coords"},
        success: function(res){//alert('2');
ajax_marker_add_response(res);}
      }); 
};

ajax_marker_add_request();

function   call_info_window(marker, info_park){
    infowindow.setContent('Parking place - '+marker.getTitle()+'<br /> Info -'+info_park+'<br />Go to payment <a href="/en/payment?parking_place='+marker.getTitle()+'"><button> Pay</button></a>'); 
	infowindow.open(map,marker); 
        
  }
  
  function addMarker(location, id_marker) {
  var marker = new google.maps.Marker({
    position: location,
    map: map,
    title: id_marker
	});
	
  google.maps.event.addListener(marker, 'click', function(event) {
  ajax_init_info(marker,id_marker);
//  call_info_window(marker); 
  }); 
  markers.push(marker);
  }
  
  // Sets the map on all markers in the array.
function setAllMap(map) {
  for (var i = 0; i < markers.length; i++) {
    markers[i].setMap(map);
  }
}

// Removes the markers from the map, but keeps them in the array.
function clearMarkers() {
  setAllMap(null);
}

// Shows any markers currently in the array.
function showMarkers() {
  setAllMap(map);
}

// Deletes all markers in the array by removing references to them.
function deleteMarkers() {
  clearMarkers();
  markers = [];
}
  
  function showInContentWindow(text) {
    var sidediv = document.getElementById('content-window');
    sidediv.innerHTML = sidediv.innerHTML+"<p>"+text;
  }
}

google.maps.event.addDomListener(window, 'load', initialize);
