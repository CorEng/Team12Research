var dublin = {lat: 53.349605, lng:-6.264175 };

// Geolocation variable
var pos;

// Date and time of search
var dateTime;

// Locations entered by the user
var posA = {};
var posB = {};

// Data returned by the google call in the back end
var googleData;

// Data of intermediate stops worked out in the back end with google data
var intermediateStops;

var nowDayTime;
var hrs;
var mins;

function refreshMap() {
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
    })
}


// Display current time and current date in search form
function displayNowTimeDate() {

    nowDayTime = new Date();
    hrs = nowDayTime.getHours().toString();
    mins = nowDayTime.getMinutes().toString();
    if (mins.length < 2) {
        mins = "0"+ mins;
    }

    document.querySelector("#time").value = hrs + ":" + mins;
    document.querySelector("#date").valueAsDate = nowDayTime;
}



// Initialize and add the map
function initMap() {
    directionsService = new google.maps.DirectionsService();
    directionsDisplay = new google.maps.DirectionsRenderer();

    refreshMap();

    // start the user's geolocations-------------------------------------------
    infoWindow = new google.maps.InfoWindow;

    // Try HTML5 geolocation.
    if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
        pos = {
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

// Draw the polylines from the back end google maps directions api call
function draw_poly(googleData, option) {
    if (option === undefined) {
        option = 0;
    }
    var linebounds = new google.maps.LatLngBounds();
    linebounds.extend(googleData['routes'][option]['bounds']['northeast']);
    linebounds.extend(googleData['routes'][option]['bounds']['southwest']);
    map.fitBounds(linebounds);
    for (var i = 0; i < googleData['routes'][option]['legs'][0]['steps'].length; i++) {
//        IF its walking draw polyline with a certain color
        if (googleData['routes'][option]['legs'][0]['steps'][i]['travel_mode'] == 'WALKING') {
            var poli = new google.maps.Polyline({
                  path: google.maps.geometry.encoding.decodePath
                  (googleData['routes'][option]['legs'][0]['steps'][i]['polyline']['points']),
                  geodesic: true,
                  strokeColor: '#ff6600',
                  strokeOpacity: 0.5,
                  strokeWeight: 5
                });
                poli.setMap(map);
        }
//        If its by bus draw the polyline with a certain colour
        else if (googleData['routes'][option]['legs'][0]['steps'][i]['travel_mode'] == 'TRANSIT') {
            var poli = new google.maps.Polyline({
                  path: google.maps.geometry.encoding.decodePath
                  (googleData['routes'][option]['legs'][0]['steps'][i]['polyline']['points']),
                  geodesic: true,
                  strokeColor: '#0000cc',
                  strokeOpacity: 0.5,
                  strokeWeight: 5
                });
                poli.setMap(map);
        }
    }
    window.scrollTo(0, 700);
}

function draw_markers(intermediateStops, option) {
    if (option === undefined) {
        option = 0;
    }
    var infowindow = new google.maps.InfoWindow();
    for (var i = 0; i < intermediateStops[option].length; i++) {
        for (var j = 0; j < intermediateStops[option][i].length; j++) {

            var location = {lat: intermediateStops[option][i][j][0], lng: intermediateStops[option][i][j][1]};
            var marker = new google.maps.Marker({animation: google.maps.Animation.DROP, position: location, map: map});

            var name = intermediateStops[option][i][j][6];
            var going = intermediateStops[option][i][j][4];
            var stopNum = intermediateStops[option][i][j][2].slice(-4);

            var contentString = '<div class="infoWin">' +
                                '<p class="detail">STOP NAME: ' + name + '</p>' +
                                '<p class="detail">GOING TO: ' + going + '</p>' +
                                '<p class="detail">STOP NO: ' + stopNum + '</p>' +
                                '</div>';

            google.maps.event.addListener(marker, 'click', (function(contentString, marker, i) {
                return function() {

                    infowindow.setContent(contentString.toString());
                    infowindow.open(map, marker);
                }
            })(contentString, marker, i));
        }
    }
}

// Create the html to show the different options with minimal info
function showOptions() {
console.log(googleData);
    if (googleData) {
        var countOps = 0;
//        Build the options buttons
        for (var i = 0; i < googleData['routes'].length; i++) {
            var div = document.createElement("div");
            div.setAttribute("class", "opbutt");
            div.setAttribute("onClick", "chooseOption(" + i.toString() + ")");

            var allSteps = document.createElement("div");
            allSteps.setAttribute("class", "allsteps");
            allSteps.setAttribute("id", "allSteps"+i.toString())

            var indiv1 = document.createElement("div");
            indiv1.setAttribute("class", "indivleft");
            var time = document.createElement("p");
            var timetext = document.createTextNode(googleData['routes'][i]['legs'][0]['duration']['text']);
            time.appendChild(timetext);
            indiv1.appendChild(time);
            div.appendChild(indiv1);

            var indiv2 = document.createElement("div");
            indiv2.setAttribute("class", "indivmid");
            var time = document.createElement("p");
            var timetext = document.createTextNode(googleData['routes'][i]['legs'][0]['departure_time']['text'] + " to "
            + googleData['routes'][i]['legs'][0]['arrival_time']['text']);
            time.appendChild(timetext);
            indiv2.appendChild(time);
            div.appendChild(indiv2);

            var indiv3 = document.createElement("div");
            indiv3.setAttribute("class", "indivright");
            var buses = document.createElement("p");
            var allBuses = [];
            for (var j = 0; j < googleData['routes'][i]['legs'][0]['steps'].length; j++ ) {

                var step = document.createElement("p");
                var stepOff = document.createElement("p");

                if (googleData['routes'][i]['legs'][0]['steps'][j]['travel_mode'] == 'WALKING' && j ==
                googleData['routes'][i]['legs'][0]['steps'].length - 1) {
                    var instruction = document.createTextNode
                    (googleData['routes'][i]['legs'][0]['steps'][j]['html_instructions']);
                    step.appendChild(instruction);
                    allSteps.appendChild(step);
                }
                else if (googleData['routes'][i]['legs'][0]['steps'][j]['travel_mode'] == 'WALKING') {
                    var instruction = document.createTextNode
                    (googleData['routes'][i]['legs'][0]['steps'][j]['html_instructions'] + " Bus Stop");
                    step.appendChild(instruction);
                    allSteps.appendChild(step);
                }
                else if (googleData['routes'][i]['legs'][0]['steps'][j]['travel_mode'] == 'TRANSIT') {
                    var instruction = document.createTextNode
                    ("Get On Bus " +  googleData['routes'][i]['legs'][0]['steps'][j]['transit_details']
                    ['line']['short_name'] + googleData['routes'][i]['legs'][0]['steps'][j]['html_instructions']
                    .substring(3));

                    var off = document.createTextNode
                    ("Get Off At " + googleData['routes'][i]['legs'][0]['steps'][j]['transit_details']
                    ['arrival_stop']['name'] + " Bus Stop");

                    step.appendChild(instruction);
                    allSteps.appendChild(step);
                    stepOff.appendChild(off);
                    allSteps.appendChild(stepOff);

                    allBuses.push(googleData['routes'][i]['legs'][0]['steps'][j]['transit_details']['line']
                    ['short_name']);
                }



            }
            var timetext = document.createTextNode(allBuses.join(" / "));
            buses.appendChild(timetext);
            indiv3.appendChild(buses);
            div.appendChild(indiv3);

//            Filter the options to show the ones that use the bus number given in search form and display first on map
//            that fits the chosen bus number
            var routeNeeded = document.getElementById("route").value;
            if (routeNeeded.length > 0) {
                if (allBuses.includes(routeNeeded) == true) {
                    document.getElementById('ops').appendChild(div);
                    document.getElementById('ops').appendChild(allSteps);
                    countOps++;
                    if (countOps == 1) {
                        chooseOption(i);
                    }
                }
            }
//            If no specific bus number input in search form show all options in list and display 1st on map
            else if (routeNeeded.length < 1) {
                document.getElementById('ops').appendChild(div);
                document.getElementById('ops').appendChild(allSteps);
                countOps++;
                if (countOps == 1) {
                    chooseOption(i);
                }
            }
        }
        window.scrollTo(0, 700);
        $("div.variable").slideDown("slow");

        if (countOps < 1) {
            window.alert("The Quickest Options Don't Use the Bus You Specified! - PLEASE TRY SEARCHING AGAIN WITHOUT A "
             +
            "SPECIFIC BUS NUMBER TO SEE THE BEST OPTIONS")
        }
    } else {
        document.getElementById('ops').style.display = 'none';
    }
}


function showSteps(num) {

    if ( $("#allSteps"+num.toString()).css("display") != "none") {
            $("#allSteps"+num.toString()).slideUp("slow");
        }
    else {
    $(".allsteps").not("#allSteps"+num.toString()).slideUp("slow")
            $("#allSteps"+num.toString()).slideDown("slow");
    }
}


function chooseOption(num) {

    refreshMap();

//  Draw markers and polylines of a specific option chosen
    showSteps(num);
    draw_markers(intermediateStops, num);
    draw_poly(googleData, num);
    window.scrollTo(0, 1100);
}


function checkDateAndTime() {
    formTime = document.getElementById("time").value;
    formDate = document.getElementById("date").value;

    var formMonth = parseInt(formDate.substring(5,7));
    var nowMonth = nowDayTime.getMonth()+1;
    var formDay = parseInt(formDate.substring(8));
    var nowDay = nowDayTime.getDate();

    var formHour = parseInt(formTime.substring(0,2));
    var nowHour = nowDayTime.getHours();
    var formMins = parseInt(formTime.substring(3));
    var nowMins = nowDayTime.getMinutes();

    if ((formMonth < nowMonth) || (formMonth == nowMonth && formDay < nowDay) || (formMonth == nowMonth && formDay ==
    nowDay && formHour < nowHour) || (formMonth == nowMonth && formDay == nowDay && formHour == nowHour && formMins
    < nowMins)) {
        alert("INVALID DATE - DATE CANNOT BE IN THE PAST");
    } else {
        return true
    }
}


// Send the directions from/to to the back end to obtain the intermediate stops for each option
function ajax() {
    $("div.variable").slideUp("slow");
//  Remove the previous options displayed
    $('div').remove(".opbutt");
    $('div').remove(".allsteps");
//  Refresh map
    if (intermediateStops) {
        refreshMap();
    }

//    Check that the user has input a value otherwise use the geolocation coordinates
    var origin = document.getElementById("start").value;

    if (origin.length > 0) {
        postA = origin;
    } else if (origin.length < 1) {
        postA = pos['lat'].toString() + "," + pos['lng'].toString();
    }
    if (checkDateAndTime() == true) {
    //    Ajax pass variables to Flask back end
        $.getJSON($SCRIPT_ROOT + '/directions', {
            postA,
            postB: document.getElementById("end").value,
            htmlTime: document.getElementById("time").value,
            htmlDate: document.getElementById("date").value,
        },
    //  Response from the back end
        function(response) {
            googleData = response['gooData'];
            intermediateStops = response['interstops'];
            showOptions();
        });
    };
}

$("input").click(displayNowTimeDate);


