const { app, BrowserWindow, dialog, Menu, ipcMain, shell } = require('electron')
const fs = require("fs")

var currentFile = undefined

function newFile(win) {
    win.webContents.send("newFile")
    currentFile = undefined
}

function openFile(win) {
    const files = dialog.showOpenDialogSync(win, {
        properties: ['openFile'],
        filters: [{
            name: "Doggoscript File",
            extensions: ["ds"]
        }]
    }); 

    if (!files) {
        return;
    };

    const file = files[0];
    const fileContent = fs.readFileSync(file).toString();
    win.webContents.send("openFile", fileContent)
    currentFile = file
}

function saveFile(win) {
    if (currentFile == undefined) {
        const file = dialog.showSaveDialogSync(win, {
            filters: [{
                name: "Doggoscript File",
                extensions: ["ds"]
            }]
        });

        if (!file) {
            return;
        };

        win.webContents.send("getContent");

        ipcMain.on("recieveContent", (event, content) => {
            fs.writeFileSync(file, content)
        });

        currentFile = file
    } else {
        win.webContents.send("getContent");

        ipcMain.on("recieveContent", (event, content) => {
            fs.writeFileSync(currentFile, content)
        });
    }
}

function saveFileAs(win) {
    const file = dialog.showSaveDialogSync(win, {
        filters: [{
            name: "Doggoscript File",
            extensions: ["ds"]
        }]
    });

    if (!file) {
        return;
    };

    win.webContents.send("getContent");

    ipcMain.on("recieveContent", (event, content) => {
        fs.writeFileSync(file, content)
    });

    currentFile = file
}

function runScript(win) {
    if (currentFile == undefined) {
        saveFileAs(win)
    }
    const currentFileSplit = currentFile.split("\\")
    const fileName = currentFileSplit[currentFileSplit.length - 1]
    //fs.copyFileSync(currentFile, app.getAppPath() + `\\run\\${fileName}`)
    //shell.openPath(app.getAppPath() + `\\run\\run_script.bat ${app.getAppPath()}\\run ${fileName}`)
    var child = require('child_process').execFile(`${app.getAppPath()}\\run\\run_script.bat`, [ 
        app.getAppPath()+'\\run', fileName ]); 
    // use event hooks to provide a callback to execute when data are available: 
    child.stdout.on('data', function(data) {
        console.log(data.toString());
    });
    require("child_process").execSync(`cmd /c start "" cmd /c ${app.getAppPath()}\\run\\run_script.bat ${app.getAppPath()}\\run ${fileName}`)
    fs.unlinkSync(app.getAppPath() + "\\run\\" + fileName)
}

function create_menu(win) {
    const template = [
        {

            label: 'File',
            submenu: [
                {
                    label: "New",
                    accelerator: "Ctrl+N",
                    click() {
                        newFile(win)
                    }
                },
                {
                    label: "Open",
                    accelerator: "Ctrl+O",
                    click() {
                        openFile(win);
                    }
                },
                {
                    label: "Save",
                    accelerator: "Ctrl+S",
                    click() {
                        saveFile(win);
                    }
                },
                {
                    label: "Save as",
                    accelerator: "Ctrl+Shift+S",
                    click() {
                        saveFileAs(win)
                    }
                },
                { type: "separator" },
                {
                    label: "Run",
                    accelerator: "F5",
                    click() {
                        runScript(win)
                    }
                },
                { type: "separator" },
                { role: 'quit' }
            ]
        },
        {
            label: "Edit",
            submenu: [
                { role: "undo" },
                { role: 'redo' },
                { type: 'separator' },
                { role: 'cut' },
                { role: 'copy' },
                { role: 'paste' },
                { role: 'delete' },
                { type: 'separator' },
                { role: 'selectAll' }
            ]
        },
        {
            label: 'View',
            submenu: [
                { role: 'resetzoom' },
                { role: 'zoomin' },
                { role: 'zoomout' },
                { type: 'separator' },
                { role: 'togglefullscreen' }
            ]
        },
        {
            label: "Developer",
            submenu: [
                {
                    label: "Toggle Developer Tools",
                    accelerator: "Ctrl+Shift+I",
                    click() {
                        win.webContents.toggleDevTools()
                    }
                }
            ]
        }
    ]
    const menu = Menu.buildFromTemplate(template)
    return menu
}

function createWindow() {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true
        }
    })

    win.loadFile('index.html')
    win.setMenu(create_menu(win))
}

app.whenReady().then(createWindow)

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit()
    }
})

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow()
    }
})