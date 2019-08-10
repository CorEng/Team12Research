var cookieCount = 0;


function setCookie() {
    if (cookieCount < 6) {
        if (googleData === "undefined" || disruptions === "undefined") {
            alert("No previous search to save in this session - please make a search in order to save it")
        }
        else {
            document.cookie = "cookieNo=" + cookieCount.toString() + "; gooleData=" +  googleData.toString() +
            "; disruptions=" + disruptions.toString();
        }
    }
    else {
        alert("Apologies you can only save 5 searches")
    }
}