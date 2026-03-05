
//code for menu toggle 
function menuToggle(){
    var menu = document.getElementById('menuLinks');
    if (menu.style.display === "block"){
        menu.style.display = 'none';
    } else {
        menu.style.display = "block";
    }
}

//logo colour to change when not on homepage
function logoColour(){
    const logo = document.querySelector('.logo');
    const isHome = window.location.pathname === '/';

    if(logo && isHome){
        logo.style.borderBottomColor = '#234473'
    } else {
        logo.style.borderBottomColor = '#7AACD3'
    }
}

window.addEventListener('DOMContentLoaded', logoColour);
