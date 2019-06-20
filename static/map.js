// Initialize and add the map
function initMap() {
    // The location of Ireland--------------------------------------------
    var ireland = {lat: 53.2734, lng: -7.77832031};

    // The map, centered at Ireland
    var map = new google.maps.Map(
        document.getElementById('map'), {zoom: 12, center: ireland});


    var infowindow = new google.maps.InfoWindow();

    // 1/3 to center map around the markers
    var bounds = new google.maps.LatLngBounds();

    // place different stations markers on the map
    for (var i = 0; i < latLonStops.length; i++) {
        var location = {lat: latLonStops[i][0], lng: latLonStops[i][1]};
        // 2/3 center map around the markers
        bounds.extend(location);
        var marker = new google.maps.Marker({animation: google.maps.Animation.DROP, position: location, map: map});

        google.maps.event.addListener(marker, 'click', (function(marker, i) {
            return function() {
                infowindow.setContent('<div>' +
                '<p class="detail">' + latLonStops[i][2] + '</p>' +
                '</div>');
                infowindow.open(map, marker);
            }
        })(marker, i));

        // 3/3 center map around the markers
        //map.fitBounds(bounds);
     }


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
    }// initMap()

    function handleLocationError(browserHasGeolocation, infoWindow, pos) {
        infoWindow.setPosition(pos);
        infoWindow.setContent(browserHasGeolocation ?
                          'Error: The Geolocation service failed.' :
                          'Error: Your browser doesn\'t support geolocation.');
        infoWindow.open(map);
        }
