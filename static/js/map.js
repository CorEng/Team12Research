var dublin = {lat: 53.349605, lng:-6.264175 };
var posA = {};
var posB = {};

// Initialize and add the map
function initMap() {
    directionsService = new google.maps.DirectionsService();
    directionsDisplay = new google.maps.DirectionsRenderer();

    // The map, centered at Dublin
    map = new google.maps.Map(
        document.getElementById('map'), {zoom: 13, center: dublin,
          zoomControl: true,
          mapTypeControl: true,
          mapTypeControlOptions: {
          style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
          },
          scaleControl: true,
          streetViewControl: true,
          streetViewControlOptions: {
          position: google.maps.ControlPosition.RIGHT_CENTER
          },
          rotateControl: true,
          fullscreenControl: true
        });

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


function ajax2(result) {
    $.getJSON($SCRIPT_ROOT + '/directions', result);
}


// Google Directions
function calcRoute() {

    var start = posA;
    var end = posB;

    var request = {
        origin: start,
        destination: end,
        provideRouteAlternatives: true,
        travelMode: 'TRANSIT',
        transitOptions: {
            modes: ['BUS'],
            routingPreference: 'FEWER_TRANSFERS'
          },
      };

    directionsService.route(request, function(result, status) {
        if (status == 'OK') {
          directionsDisplay.setDirections(result);
          window.scrollTo(0, 700);
        } else {
          window.alert('Directions request failed due to ' + status);
        }
      });
    }

// Take input from origin of trip
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

// Take input from Destination of trip
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

function ajax() {
//    calcRoute();
    $.getJSON($SCRIPT_ROOT + '/directions', {
        postA: document.getElementById("start").value,
        postB: document.getElementById("end").value
    }, function(response) {
    console.log(response);
        var linebounds = new google.maps.LatLngBounds();
        linebounds.extend(response['routes'][0]['bounds']['northeast']);
        linebounds.extend(response['routes'][0]['bounds']['southwest']);
        map.fitBounds(linebounds);
        for (var i = 0; i < response['routes'][0]['legs'][0]['steps'].length; i++) {
            var poli = new google.maps.Polyline({
                  path: google.maps.geometry.encoding.decodePath
                  (response['routes'][0]['legs'][0]['steps'][i]['polyline']['points']),
                  geodesic: true,
                  strokeColor: '#0000cc',
                  strokeOpacity: 0.6,
                  strokeWeight: 5
                });
                poli.setMap(map);
        }
    });
    window.scrollTo(0, 700);
}

google.maps.event.addDomListener(window, 'load', calcRoute);

