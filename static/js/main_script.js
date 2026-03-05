// //menu icon
// function mainToggle(e) {
//     e.preventDefault();
//     document.getElementById("menuLinks").classList.toggle("open");
// }

//hide menu icon once clicked
document.getElementById("menuToggle").addEventListener("click", function (e) {
    e.preventDefault();

    const menu = document.getElementById("menuLinks");
    const icon = document.getElementById("menuToggle");

    menu.classList.toggle("open");

    if (menu.classList.contains("open")) {
        icon.classList.add("hidden");
    } else {
        icon.classList.remove("hidden");
    }
});


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
