// //menu icon
// function mainToggle(e) {
//     e.preventDefault();
//     document.getElementById("menuLinks").classList.toggle("open");
// }

//hide menu icon once clicked
document.getElementById("menuToggle").addEventListener("click", function (e) {
    e.preventDefault();

    const menu = document.getElementById("menuLinks");
    const icon = document.getElementById("menuToggle svg");

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
    const isMunros = window.location.pathname === '/munros/';

    if(logo && isHome){
        logo.style.borderBottomColor = '#234473'
    } else if(logo && isMunros){
        logo.style.borderBottomColor = '#4D86BB'
    } else {
        logo.style.borderBottomColor = '#A3CAE1'
    }
}

//menu toggle colour to change when not on homepage
function navColour(){
    const nav = document.querySelector('.nav-bar path');
    const isHome = window.location.pathname === '/';
    const isMunros = window.location.pathname === '/munros/';

    if(nav && isHome){
        nav.style.color = '#234473'
    } else if(nav && isMunros){
        nav.style.color = '#4D86BB'
    } else {
        nav.style.color = '#A3CAE1'
    }
}


//add climb modal information
var modal = document.getElementById("addClimb");
var btn = document.getElementById("modalBtn");
var span = document.getElementsByClassName("close")[0];

btn.onclick = function(){
    modal.style.display = "block";
    document.body.classList.add("modal-open");
}

span.onclick = function(){
    modal.style.display = 'none';
    document.body.classList.remove("modal-open");
}

window.onclick = function(event){
    if (event.target == modal){
        modal.style.display = 'none';
        document.body.classList.remove("modal-open");
    }
}

//mountain triangles to change when not on profile page
// function mountainTris(){
//     const triangle = document.querySelector('.base-triangle');
//     const background = document.querySelector('.mountains');
//     const isProfile = window.location.pathname === '/profile/' || window.location.pathname === '/profile';

//     triangle.forEach(tri => {
//         tri.style.borderBottomColor = isProfile ? '#A3CAE1' : '#4D86BB';
//     });

//     if(background && isProfile){
//         background.style.backgroundColor = '#A3CAE1'
//     } else {
//         background.style.backgroundColor = '#4D86BB'
//     }
// }


window.addEventListener('DOMContentLoaded', () => {
    logoColour();
    mountainTris();
    navColour();
});
