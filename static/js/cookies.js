function getCount() {
    var count = 0
    for (var i = 0; i < 5; i++) {
        if (localStorage.getItem("cookie" + i.toString())) {
            count++;
        }
    };
    return count;
};


function setCookies() {
    var count = getCount();
    if (count < 4) {
        var variableList = [googleData, intermediateStops, disruptions, backAmenities];
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
}

function getCookie(num) {
    var x = JSON.parse(localStorage.getItem("cookie" + num.toString()));
    googleData = x[0];
    intermediateStops = x[1];
    disruptions = x[2]
    backAmenities = x[3];
    showOptions();
}

function removeCookie(num) {
    localStorage.removeItem("cookie" + num.toString());
}

function clearAll() {
    localStorage.clear();
}

