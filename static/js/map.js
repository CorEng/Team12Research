// The location of Ireland--------------------------------------------
var dublin = {lat: 53.349605, lng:-6.264175 };
var posA = {};
var posB = {};

// Initialize and add the map
function initMap() {
    directionsService = new google.maps.DirectionsService();
    directionsDisplay = new google.maps.DirectionsRenderer();

    // The map, centered at Dublin
    var map = new google.maps.Map(
        document.getElementById('map'), {zoom: 12, center: dublin});

    // start the user's geolocations-------------------------------------------
    infoWindow = new google.maps.InfoWindow;

    // Try HTML5 geolocation.
    if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
        var pos = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
        };

        infoWindow.setPosition(pos);
        infoWindow.setContent('You are here');
        infoWindow.open(map);
        map.setCenter(pos);
    }, function() {
    handleLocationError(true, infoWindow, map.getCenter());
    });
    } else {
    // Browser doesn't support Geolocation
    handleLocationError(false, infoWindow, map.getCenter());
        }
    directionsDisplay.setMap(map);
    };// initMap()



function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(browserHasGeolocation ?
                      'Error: The Geolocation service failed.' :
                      'Error: Your browser doesn\'t support geolocation.');
    infoWindow.open(map);
    }


function calcRoute() {
    var start = posA;
    var end = posB;

    var request = {
        origin: start,
        destination: end,
        travelMode: 'TRANSIT'
      };

    directionsService.route(request, function(result, status) {
        if (status == 'OK') {
          directionsDisplay.setDirections(result);
        }
      });
    }

function stopA(){

    // AutoComplete------------------------------------------------------------
    var input = document.getElementById('start');

    var dublinBounds = new google.maps.LatLngBounds(
      new google.maps.LatLng(53.1235, -6.5021),
      new google.maps.LatLng(53.4872, -6.0209));

    var defaultBounds = {
    bounds: dublinBounds,
    strictBounds: true
    };

    var autocomplete = new google.maps.places.Autocomplete(input, defaultBounds);

    google.maps.event.addListener(autocomplete, 'place_changed', function() {
      var place = autocomplete.getPlace();
      var lat = place.geometry.location.lat();
      var lng = place.geometry.location.lng();
      posA = {
      	lat: lat,
      	lng: lng
      	};
        });
    }

function stopB(){

    // AutoComplete------------------------------------------------------------
    var input = document.getElementById('end');

    var dublinBounds = new google.maps.LatLngBounds(
      new google.maps.LatLng(53.1235, -6.5021),
      new google.maps.LatLng(53.4872, -6.0209));

    var defaultBounds = {
    bounds: dublinBounds,
    strictBounds: true
    };

    var autocomplete = new google.maps.places.Autocomplete(input, defaultBounds);

    google.maps.event.addListener(autocomplete, 'place_changed', function() {
      var place = autocomplete.getPlace();
      var lat = place.geometry.location.lat();
      var lng = place.geometry.location.lng();
      posB = {
      	lat: lat,
      	lng: lng
      	};
        });
    }

google.maps.event.addDomListener(window, 'load', calcRoute);