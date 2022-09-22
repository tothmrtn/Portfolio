/* === Check/Remove button switch function === */
function check_me(input_id) {

    var check_input = document.querySelector('input[id=' + input_id + ']');
    var check_label = document.querySelector('label[name=' + input_id  + ']');

    var btn = document.getElementById("remove_btn");

    var checkBoxes = document.getElementsByName('check');
    var selected = [];

    for (var i=0; i<checkBoxes.length; i++) {
        if (checkBoxes[i].checked) {
            selected.push(checkBoxes[i].value);
        }
    }

    if (selected.length != 0 && check_input.checked){
        check_label.style.textDecoration = "line-through";
        btn.value = "REMOVE TASK";
        btn.style.color = "#FFFFFF";
        btn.style.border = "red";
        btn.style.backgroundColor = "#FE7575";
        btn.style.cursor = "pointer";

    }else if (!(check_input.checked)){
        check_label.style.textDecoration = "";
    }

    if (selected.length == 0){
        check_label.style.textDecoration = "";
        btn.value = "CHECK TASK";
        btn.style.color = "#4db5ff";
        btn.style.backgroundColor = "transparent";
        btn.style.border = "1px solid #4db5ff";
        btn.style.cursor = "pointer";
        btn.onmouseover = function() {mouseOver()};
        btn.onmouseout = function() {mouseOut()};
    }
}



/* === Separate hover functions for Check button === */
function mouseOver() {
    button = document.getElementById("remove_btn");
    button.style.color = "#1f1f38";
    button.style.background = "#fff";
    button.style.border = "1px solid white";
}

function mouseOut() {
    button = document.getElementById("remove_btn");
    button.style.color = "#4db5ff";
    button.style.border = "1px solid #4db5ff";
    button.style.background = "transparent";
}



/* === Clock function === */
function displayTime(){
    var dateTime = new Date();

    var hrs = dateTime.getHours();
    var min = dateTime.getMinutes();
    var sec = dateTime.getSeconds();
    var session = document.getElementById('session');

    if (hrs >= 12){
        session.innerHTML = 'PM';
    }else{
        session.innerHTML = 'AM';
    }

    if (hrs > 12){
        hrs = hrs - 12;
    }

    document.getElementById('hours').innerHTML = hrs;
    document.getElementById('minutes').innerHTML = min;
    document.getElementById('seconds').innerHTML = sec;
}
setInterval(displayTime, 10);