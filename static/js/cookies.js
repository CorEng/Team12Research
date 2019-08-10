
function setCookies() {

    if (document.cookie.indexOf(";") == -1) {
        if (document.cookie.length < 1) {
            cookiesLength = 0;
        }
        else if (document.cookie.length > 0) {
            cookiesLength = 1;
        }
    }
    else {
        cookiesLength = document.cookie.split(" ").length;
    };




    console.log(document.cookie);
    console.log(cookiesLength);

    var variableList = [JSON.stringify(googleData), JSON.stringify(intermediateStops), JSON.stringify(backAmenities)];

    x = document.cookie = "cookie" + (cookiesLength).toString() + "=" + JSON.stringify(variableList);




//    if (cookiesLength == 5) {
//        alert("Apologies you have reached the max of 5 saved searches");
//    }
//    else {
//        if (variableList[0] == null) {
//            alert("No previous search available to save, please perform a search to save it");
//        }
//        else {
//
//            x = document.cookie = "cookie" + (cookiesLength).toString() + "=" + JSON.stringify(variableList);
//            console.log("after trying to save");
//            console.log(document.cookie);
//        }
//    }





//
//
//
//    console.log(JSON.parse(dataCookies)[0]);
}

function showCookies() {

}

