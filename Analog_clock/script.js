let second = 0;
let minute = 0;
let hour = 0;

let secondHand = document.getElementById("second-handle");

let minuteHand = document.getElementById("minute-handle");

let hourHand = document.getElementById("hour-handle");

setInterval(() => {
    let Current = new Date();
    second = Current.getSeconds() * 6;
    minute = Current.getMinutes() * 6;
    hour = Current.getHours() * 30 + Math.round(minute/12);

    secondHand.style.transform = "rotate(" + second + "deg)";

    minuteHand.style.transform = "rotate(" + minute + "deg)";

    hourHand.style.transform = "rotate(" + hour + "deg)";
    
}, 1000)