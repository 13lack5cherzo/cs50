
function random_body_background() {
    /*
    * function to change background colour at random
    */

    // random colour
    r = parseInt(Math.random() * 255);
    g = parseInt(Math.random() * 255);
    b = parseInt(Math.random() * 255);

    body = document.getElementsByTagName('body')[0]; // get body object
    body.style.backgroundColor = "rgb(" + r + ", " + g + ", " + b + ")"; // change colour
}


function startTime() {

    function checkTime(i) {
        if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
        return i;
    }

    const today = new Date();
    let h = today.getHours();
    let m = today.getMinutes();
    let s = today.getSeconds();
    m = checkTime(m);
    s = checkTime(s);
    document.getElementById('clock1').innerHTML =  h + ":" + m + ":" + s;
    setTimeout(startTime, 1000);
}


