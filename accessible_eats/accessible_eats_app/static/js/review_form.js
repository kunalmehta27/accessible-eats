var placeSearch, autocomplete;

var map, places, infoWindow;
var markers = [];
var autocomplete;

$(".form-page").hide()
$("#page1").show()

function initAutocomplete() {
  map = new google.maps.Map(document.getElementById('google-map'), {
    zoom: 3,
    center: {lat: 37.1, lng: -95.7},
    mapTypeControl: false,
    panControl: false,
    zoomControl: false,
    streetViewControl: false
  });

  autocomplete = new google.maps.places.Autocomplete(
      (document.getElementById('id_restaurant')),
      {types: ['establishment']});
  places = new google.maps.places.PlacesService(map);

  autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged() {
  var place = autocomplete.getPlace();
  deleteMarkers()
  addMarker(place.geometry.location)
  if (place.geometry) {
    map.panTo(place.geometry.location);
    map.setZoom(15);
  } else {
    document.getElementById('autocomplete').placeholder = 'Enter a city';
  }
}

function setMapOnAll(map) {
  for (var i = 0; i < markers.length; i++) {
    markers[i].setMap(map);
  }
}

function clearMarkers() {
  setMapOnAll(null);
}

function deleteMarkers() {
  clearMarkers();
  markers = [];
}

function addMarker(location) {
  var marker = new google.maps.Marker({
    position: location,
    map: map
  });
  markers.push(marker);
}

$("#previous-page").click(function() {
  page_num = $("#page-num").html()
  new_page_num = Math.max(1, parseInt(page_num) - 1)
  console.log(new_page_num)
  $("#page-num").html(new_page_num)
  $(".form-page").hide()
  $("#page" + new_page_num.toString()).show()
})

$("#next-page").click(function() {
  num_pages = parseInt($("#num-pages").html())
  page_num = $("#page-num").html()
  new_page_num = Math.min(num_pages, parseInt(page_num) + 1)
  $("#page-num").html(new_page_num)
  $(".form-page").hide()
  $("#page" + new_page_num.toString()).show()
})