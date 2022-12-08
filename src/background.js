"use strict";

import { app, protocol, BrowserWindow } from "electron";
import { createProtocol } from "vue-cli-plugin-electron-builder/lib";
import installExtension, { VUEJS3_DEVTOOLS } from "electron-devtools-installer";
const isDevelopment = process.env.NODE_ENV !== "production";

// Scheme must be registered before the app is ready
protocol.registerSchemesAsPrivileged([
  { scheme: "app", privileges: { secure: true, standard: true } },
]);

async function createWindow() {
  // "C:\\Users\\Gjirafa\\Desktop\\projects\\vue-electron\\server\\app.exe"
  if (isDevelopment) {
    var python = require("child_process").spawn("py", ["./resources/app.py"]);
    python.stdout.on("data", function (data) {
      console.log("data: ", data.toString("utf8"));
    });
    python.stderr.on("data", (data) => {
      console.log(`stderr: ${data}`); // when error
    });
  } else {
    let backend;
    var path = require("path");
    backend = path.join(process.cwd(), "\\resources\\app.exe");
    console.log(process.cwd());
    var execfile = require("child_process").execFile;
    execfile(
      backend,
      {
        windowsHide: true,
      },
      (err, stdout, stderr) => {
        if (err) {
          console.log(err);
        }
        if (stdout) {
          console.log(stdout);
        }
        if (stderr) {
          console.log(stderr);
        }
      }
    );
  }
  // Create the browser window.
  const win = new BrowserWindow({
    // icon: `./public/icon.png`,
    title: "Egzoni Market",
    width: 800,
    height: 600,
    webPreferences: {
      // Use pluginOptions.nodeIntegration, leave this alone
      // See nklayman.github.io/vue-cli-plugin-electron-builder/guide/security.html#node-integration for more info
      nodeIntegration: process.env.ELECTRON_NODE_INTEGRATION,
      contextIsolation: !process.env.ELECTRON_NODE_INTEGRATION,
      //Uncomment the below line later
      // devTools: isDevelopment,
    },
  });
  win.maximize();
  win.on("close", (e) => {
    if (BrowserWindow.getAllWindows().length > 1) e.preventDefault();
  });

  if (process.env.WEBPACK_DEV_SERVER_URL) {
    // Load the url of the dev server if in development mode
    await win.loadURL(process.env.WEBPACK_DEV_SERVER_URL);
    if (!process.env.IS_TEST) win.webContents.openDevTools();
  } else {
    createProtocol("app");
    // Load the index.html when not in development
    win.loadURL("app://./index.html");
  }
}

// Quit when all windows are closed.
app.on("window-all-closed", () => {
  // On macOS it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== "darwin") {
    const { exec } = require("child_process");
    exec("taskkill /f /t /im app.exe", (err, stdout, stderr) => {
      if (err) {
        console.log(err);
        return;
      }
      console.log(`stdout: ${stdout}`);
      console.log(`stderr: ${stderr}`);
    });
    app.quit();
  }
});

app.on("activate", () => {
  // On macOS it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (BrowserWindow.getAllWindows().length === 0) createWindow();
});

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on("ready", async () => {
  if (isDevelopment && !process.env.IS_TEST) {
    // Install Vue Devtools
    try {
      await installExtension(VUEJS3_DEVTOOLS);
    } catch (e) {
      console.error("Vue Devtools failed to install:", e.toString());
    }
  }
  createWindow();
});

// Exit cleanly on request from parent process in development mode.
if (isDevelopment) {
  if (process.platform === "win32") {
    process.on("message", (data) => {
      if (data === "graceful-exit") {
        app.quit();
      }
    });
  } else {
    process.on("SIGTERM", () => {
      app.quit();
    });
  }
}
