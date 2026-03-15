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
    const isMunros = window.location.pathname === '/munros/';

    if(logo && isHome){
        logo.style.borderBottomColor = '#234473'
    } else if(logo && isMunros){
        logo.style.borderBottomColor = '#4D86BB'
    } else {
        logo.style.borderBottomColor = '#A3CAE1'
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
});
