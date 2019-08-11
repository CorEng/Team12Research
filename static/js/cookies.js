
function setCookies() {
    var count = 0
    for (var i = 0; i < 5; i++) {
        if (localStorage.getItem("cookie" + i.toString())) {
            count++;
        }
    };
    if (count < 5) {
        var variableList = [googleData, intermediateStops, backAmenities];
        if (variableList[0] != null) {
            localStorage.setItem("cookie" + (count).toString(), JSON.stringify(variableList));
            count++
        }
        else {
            alert("No previous search available to save, please perform a search to save it");
        }
    }
    else {
        alert("Apologies you have reached the max of 5 saved searches");
    };
    console.log(count);













//    if (document.cookie.indexOf(";") == -1) {
//        if (document.cookie.length < 1) {
//            cookiesLength = 0;
//        }
//        else if (document.cookie.length > 0) {
//            cookiesLength = 1;
//        }
//    }
//    else {
//        cookiesLength = document.cookie.split(" ").length;
//    };



//    x = document.cookie =  "cookie" + (cookiesLength).toString() + "=" + variableList;




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

