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
        document.getElementById('map'), {zoom: 14, center: dublin});

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
    console.log(start);
    console.log(end);

    var request = {
        origin: start,
        destination: end,
        travelMode: 'TRANSIT'
//        TransitOptions: {
//            modes: ['BUS'],
//            routingPreference: 'LESS_WALKING'
//        }
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

    var autocomplete = new google.maps.places.Autocomplete(input);

    google.maps.event.addListener(autocomplete, 'place_changed', function() {
      var place = autocomplete.getPlace();
      var lat = place.geometry.location.lat();
      var lng = place.geometry.location.lng();
      posA = {
      	lat: lat,
      	lng:lng
      	};
        });
    }

function stopB(){

    // AutoComplete------------------------------------------------------------
    var input = document.getElementById('end');

    var autocomplete = new google.maps.places.Autocomplete(input);

    google.maps.event.addListener(autocomplete, 'place_changed', function() {
      var place = autocomplete.getPlace();
      var lat = place.geometry.location.lat();
      var lng = place.geometry.location.lng();
      posB = {
      	lat: lat,
      	lng:lng
      	};
        });
    }

google.maps.event.addDomListener(window, 'load', calcRoute);