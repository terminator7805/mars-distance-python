const { app, BrowserWindow, ipcRenderer } = require("electron");
const path = require("path");
const { ipcMain } = require("electron");
var mainWindow;
function createWindow() {
   mainWindow = new BrowserWindow({
    width: 400,
    height: 620,
    icon: __dirname + "/app/resources/3D_Mars.png",
    webPreferences: {
      preload: path.join(__dirname, "/app/js/preload.js"),
      devTools: true,
      nodeIntegration: true,
      contextIsolation: false,
      enableRemoteModule: false,
    },
    resizable: false,
    fullscreenable: false,
    frame: false
  });

  mainWindow.setMenuBarVisibility(false);
  mainWindow.loadFile("./app/index.html");
}

app.whenReady().then(() => {
  createWindow();

  app.on("activate", function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on("window-all-closed", function () {
  if (process.platform !== "darwin") app.quit();
});

ipcMain.on("close", (event, arg) => {
  app.quit();
});


const net = require('net');
const server = net.createServer((socket) => {
  console.log('Client connected');
  ipcMain.on("sendPython", (event, arg) => {
    socket.write(arg.toString());
  });
  socket.on('data', (data) => {
    if (data.toString() == "None") {
      socket.end();
      app.quit()
    }
    const array = data.toString().split(" ");
    mainWindow.webContents.send('receivePython', array);

  });
});

server.listen(9090, () => {
  console.log('Server started on port 9090');
});

