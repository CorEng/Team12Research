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
//        var variableList = [googleData, intermediateStops, disruptions, backAmenities];
        if (googleData != undefined) {

            var variableList = [googleData["routes"][0]["legs"][0]["start_address"], googleData["routes"][0]["legs"][0]["end_address"]];
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
    var cookie = JSON.parse(localStorage.getItem("cookie" + num.toString()));

    if (cookie != undefined) {
        console.log(cookie);
    }
    else {
        alert("No previous search available to show, please perform a search and save it");
    };
}

function removeCookie(num) {
    localStorage.removeItem("cookie" + num.toString());
}

function clearAll() {
    localStorage.clear();
}


function showFavs() {
    for (var i = 0; i < 5; i++) {
        if (localStorage.getItem("cookie" + i.toString())) {

            var item = JSON.parse(localStorage.getItem("cookie" + i.toString()));
            console.log(item);

            var favButt = document.createElement("div");
            favButt.setAttribute("class", "favButt");

            var favOri = document.createElement("div");
            indiv1.setAttribute("class", "favOri");
            var ori = document.createElement("p");
            var oriText = document.createTextNode(item[0]);
            ori.appendChild(oriText);
            favOri.appendChild(ori);
            favButt.appendChild(favOri);

            document.getElementById("favs").appendChild(favButt);


        }
    }
}

