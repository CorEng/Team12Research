
function setCookies() {
    console.log(document.cookie);

    var cookiesLength = document.cookie.length;
    console.log(cookiesLength);
    var variableList = [googleData, intermediateStops, backAmenities]

    if (cookiesLength == 5) {
        alert("Apologies you have already 5 saved searches saved")
    }
    else {
        var dataCookies = document.cookie = "cookie" + (cookiesLength -1).toString() + "=" + JSON.stringify
        (variableList);
    }




//
//
//
//    console.log(JSON.parse(dataCookies)[0]);
}

function showCookies() {

}

