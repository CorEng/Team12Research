function getCount() {
    var count = 0
    for (var i = 0; i < 5; i++) {
        if (localStorage.getItem("cookie" + i.toString())) {
            count++;
        }
    };
    return count;
};


function saveCookie() {
    var count = getCount();
    if (count < 4) {
        if (googleData != undefined) {

            var variableList = [googleData["routes"][0]["legs"][0]["start_address"],
            googleData["routes"][0]["legs"][0]["end_address"], htmlDepArr];
            localStorage.setItem("cookie" + (count).toString(), JSON.stringify(variableList));
            count++
            alert("This search has been ADDED to your Favourites")
        }
        else {
            alert("No previous search available to save, please perform a search to save it");
        }
    }
    else {
        alert("Apologies you have reached the max of 4 saved searches");
    };
}


function removeCookie(num) {
    localStorage.removeItem("cookie" + num.toString());
    showFavs();
    setTimeout(function() {
        if (getCount() > 0) {
            $("div.favourites").slideDown("slow");
        }
        else {
            alert("Favourites list is empty");
            window.scrollTo(0,0);
        }},
        950);
}


function showFavs() {

    $('div').remove(".favButt");

    for (var i = 0; i < 5; i++) {
        if (localStorage.getItem("cookie" + i.toString())) {

            var favData = JSON.parse(localStorage.getItem("cookie" + i.toString()));

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

            var favRem = document.createElement("div");
            favRem.setAttribute("class", "favRem");
            var rem = document.createElement("p");
            rem.setAttribute("onclick", "removeCookie(" + i.toString() + ")")
            var remText = document.createTextNode("Remove");
            rem.appendChild(remText);
            favRem.appendChild(rem);
            favButt.appendChild(favRem);


            document.getElementById("favs").appendChild(favButt);
        }
    };
    var elem = document.getElementById("ops");
    var pixelsElem = window.getComputedStyle(elem, null).getPropertyValue("height");
    if (pixelsElem == "auto") {
        var pixels = 0;
    }
    else {
        var pixels = parseInt(pixelsElem.slice(0, -2))
    };
    window.scrollTo(0, 1125 + pixels);

    if ($("div.favourites").css("display") != "none") {
        $("div.favourites").slideUp("slow");
    }
    else if ($("div.favourites").css("display") == "none") {
        if (getCount() == 0) {
            alert("No Search in Favourites to Show. Please Make a Search to Then Save It")
            window.scrollTo(0,0);
        }
        else {
            $("div.favourites").slideDown("slow");
        }
    };
}


function loadFav(num) {

    backAmenities = undefined;
    $("div.options").slideUp("slow");
    $("div.amenities").slideUp("slow");

    var cookie = JSON.parse(localStorage.getItem("cookie" + num.toString()));
    console.log(cookie);

    displayNowTimeDate();

    $.getJSON($SCRIPT_ROOT + '/directions', {
            postA: cookie[0],
            postB: cookie[1],
            htmlDepArr,
            htmlTime: document.getElementById("time").value,
            htmlDate: document.getElementById("date").value,
        },
    //  Response from the back end
        function(response) {
            googleData = response['gooData'];
            intermediateStops = response['interstops'];
            disruptions = response["disruptions"];

            showOptions();
        })



}












//function clearAll() {
//    localStorage.clear();
//}

//function getCookie(num) {
//    var cookie = JSON.parse(localStorage.getItem("cookie" + num.toString()));
//
//    if (cookie != undefined) {
//        console.log(cookie);
//    }
//    else {
//        alert("No previous search available to show, please perform a search and save it");
//    };
//}
