function initialize() {
  var myLatlng = new google.maps.LatLng(49.8392491,24.0300454);
  var mapOptions = {
    zoom: 12,
    center: myLatlng
  };

  var map = new google.maps.Map(document.getElementById('map-canvas'),
      mapOptions);
  var markers = [];
  var markers_lat = [49.8392491,49.8393491,49.8352491];
  var markers_lng = [24.0300454,24.0303454,24.0305454];
  var markers_id = [0,1,2];
  
  function getRandom(min, max)
{
  return Math.random() * (max - min) + min;
}
  
  for (var j =0;j<100;j++)
  {
  markers_lat.push(getRandom(-90,90)  );
  markers_lng.push(getRandom(-90,90)  );
  markers_id.push(j+3);
  }
//  var count = 0;
  
  var contentString = '';//marker.getTitle() +'test string <button>sdcsdcs</button>';  
  var infowindow = new google.maps.InfoWindow({
      content: contentString,
  });
  
  for (var i =0; i<markers_id.length; i++){
  addMarker(new google.maps.LatLng(markers_lat[i],markers_lng[i]),markers_id[i]);
  }
  
/*  google.maps.event.addListener(map, 'click', function(event) {
    //var text = '(49.855029282036746, 24.038772583007812)';//event.latLng;
    var marker_Latlng = new google.maps.LatLng(49.8392491,24.0300454);
	var text = marker_Latlng;
	
	showInContentWindow(text);
	addMarker(marker_Latlng, count);//event.latLng
	count++;
  });
*/ 
  //todo here goes ajax
  function   call_info_window(marker){
	infowindow.setContent(marker.getTitle() +'test string <button onclick=alert("sas")>sdcsdcs</button>'); 
	infowindow.open(map,marker);  
  }
  
  function addMarker(location, id_marker) {
  var marker = new google.maps.Marker({
    position: location,
    map: map,
    title: ""+id_marker
	});
	
  google.maps.event.addListener(marker, 'click', function(event) {
  call_info_window(marker);
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