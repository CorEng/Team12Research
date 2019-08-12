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
        alert("Apologies you have reached the max of 4 saved searches");
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

    $('div').remove(".favButt");

    for (var i = 0; i < 5; i++) {
        if (localStorage.getItem("cookie" + i.toString())) {

            var favData = JSON.parse(localStorage.getItem("cookie" + i.toString()));
            console.log(favData);

            var favButt = document.createElement("div");
            favButt.setAttribute("class", "favButt");
            favButt.setAttribute("onclick", "loadFav(" + i.toString() + ")");

            var favOri = document.createElement("div");
            favOri.setAttribute("class", "favOri");
            var ori = document.createElement("p");
            var oriText = document.createTextNode(favData[0]);
            ori.appendChild(oriText);
            favOri.appendChild(ori);
            favButt.appendChild(favOri);

            var favDest = document.createElement("div");
            favDest.setAttribute("class", "favDest");
            var dest = document.createElement("p");
            var destText = document.createTextNode(favData[1]);
            dest.appendChild(destText);
            favDest.appendChild(dest);
            favButt.appendChild(favDest);


            document.getElementById("favs").appendChild(favButt);


        }
    }
}

