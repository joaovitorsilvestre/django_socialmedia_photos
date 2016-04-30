function login_over(on) {
    var login_button = document.getElementById("login_button")
    if (on == true){
        login_button.style.backgroundColor = "#439AAB"
    }
    else{
        login_button.style.backgroundColor = "#204A52"
    }
}

function display_search(on) {
    var display_search_box = document.getElementById("display_search_box")
    if (on == true){
      display_search_box.style.display = "inline"
    }
    else {
      display_search_box.style.display = "none"
    }
}

function teste() {
    var bnt = document.createElement("BUTTON");
    var b_t = document.createElement(results[0]);

    bnt.appendChild(b_t);
    var display_search_box = document.getElementById('display_search_box');
    display_search_box.appendChild(bnt);

    //return results[0]
}
