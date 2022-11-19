let authBtn = document.querySelector("#authorize")
let nav = document.querySelector(".nav")
let auth = document.querySelector(".authorization")
let authCancelBtn = document.querySelector("#close-auth")
let loginBtn = document.querySelector(".form-buttons button:first-child")
let hwinfoBtn = document.querySelector("#hw-info")
let hwinfoForm = document.querySelector(".hw-info")
let saveBtn = document.querySelector("#save-btn")
let closeHwBtn = document.querySelector("#close-hwinfo")
let quitBtn = document.querySelector("#quit")
let runBtn = document.querySelector("#run")
let statusPage = document.querySelector(".status-page")
let statusPageQuit = document.querySelector(".quit-button")
let statusForm = document.querySelector(".status-form")

eel.expose(hello_line); // Expose this function to Python
function hello_line(email) {
    if (email !== "" && email !== null) {
        document.querySelector(".header h6").innerHTML = "Hello, " + email;
    }
}

eel.expose(changeStatus);
function changeStatus(status) {
    statusForm.value = status;
}

// window.onresize = function (){
//     if (window.outerWidth !== 400 || window.outerHeight !== 600){
//         window.resizeTo(400, 600);
//     }
// }

// document.oncontextmenu = cmenu; function cmenu() {
//     return false;
// }

function hiveNav() {
    nav.style.opacity = 0;
    window.setTimeout(function (){
        nav.style.display = "none";
    }, 400)
}

function showNav() {
    window.setTimeout(function (){
        nav.style.display = "flex";
    }, 400)

    window.setTimeout(function () {
        nav.style.opacity = 1;
    }, 600)
}

function showAuth() {
    hiveNav()
    window.setTimeout(function (){
        auth.style.display = "flex";
    }, 400)

    window.setTimeout(function () {
        auth.style.opacity = 1;
    }, 600)
}

function closeAuth() {
    let emailForm = document.querySelector(".email label input")
    let passwordForm = document.querySelector(".password label input")
    let rememberMe = document.querySelector(".remember-me label input")

    auth.style.opacity = 0;
    window.setTimeout(function (){
        auth.style.display = "none";
    }, 400)

    showNav()

    emailForm.value = ""
    passwordForm.value = ""
    rememberMe.checked = false
}

function getAuthInfo() {
    let email = document.querySelector(".email label input").value
    let password = document.querySelector(".password label input").value
    let rememberMe = document.querySelector(".remember-me label input").checked
    eel.login_and_password_writer(email, password, rememberMe)
    closeAuth()
    if (email !== "" && email !== null) {
        document.querySelector(".header h6").innerHTML = "Hello, " + email;
    }
}

function getHomeworkInfo() {
    let homeworkNameForm = document.querySelector(".hw-name label input")
    let studListForm = document.querySelector(".stud-list label textarea")
    let levelsCntForm = document.querySelector(".levels-cnt label select")

    eel.get_homework_data(homeworkNameForm.value, levelsCntForm.value, studListForm.value)

    closeHwInfo()
}

function showHW() {
    hiveNav()

    window.setTimeout(function (){
        hwinfoForm.style.display = "flex";
    }, 400)

    window.setTimeout(function () {
        hwinfoForm.style.opacity = 1;
    }, 600)
}

function closeHwInfo() {

    hwinfoForm.style.opacity = 0;
    window.setTimeout(function (){
        hwinfoForm.style.display = "none";
    }, 400)
    showNav()
}

function runningApp() {
    hiveNav()

    window.setTimeout(function (){
        statusPage.style.display = "flex";
    }, 400)

    window.setTimeout(function () {
        statusPage.style.opacity = 1;
    }, 600)
}

function quitApp() {
    eel.quit_app()
    window.close()
}

authBtn.addEventListener('click', showAuth)
loginBtn.addEventListener('click', getAuthInfo)
authCancelBtn.addEventListener('click', closeAuth)

hwinfoBtn.addEventListener('click', showHW)
closeHwBtn.addEventListener('click', closeHwInfo)
saveBtn.addEventListener('click', getHomeworkInfo)

runBtn.addEventListener('click', runningApp)

quitBtn.addEventListener('click', quitApp)
statusPageQuit.addEventListener('click', quitApp)
