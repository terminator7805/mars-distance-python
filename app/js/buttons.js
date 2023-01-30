const { ipcRenderer } = require("electron");

const ipc = require("electron").ipcRenderer;
function closeApp(e) {
  e.preventDefault();
  ipc.send("close");
}
var live = false;
var interval = null;
function sendPython(arg) {
    if (arg == "live") {
        live = true;
    } else {
        live = false;
    }
    if (live) {
        if (interval == null) {
            interval = setInterval(() => {
                const timeElapsed = Date.now();
                const today = new Date(timeElapsed);
                ipc.send("sendPython", today.toISOString());
            }, 1000);
        }
    } else if (!live){
        clearInterval(interval);
        interval = null;
        var data = {
            date: document.getElementById("dateform").value.split("-"),
            hour: document.getElementById("hourform").value.split(":"),
        }
        var date = new Date(parseInt(data.date[0]), parseInt(data.date[1]) - 1, parseInt(data.date[2]), parseInt(data.hour[0]), parseInt(data.hour[1]), 0, 0);
        ipc.send("sendPython", date.toISOString());
    }
}

ipcRenderer.on("receivePython", (event, arg) => {
    const km = arg[0];
    const ua = arg[1];
    document.getElementById("km").innerHTML = parseFloat(km).toFixed(4);
    document.getElementById("ua").innerHTML = parseFloat(ua).toFixed(8);
})  
document.getElementById("live").addEventListener("click", function (e) { e.preventDefault(); sendPython('live') });
document.getElementById("submitdate").addEventListener("click", function (e) { 
     e.preventDefault();
     sendPython('date');
});
document.getElementById("close").addEventListener("click", closeApp);
