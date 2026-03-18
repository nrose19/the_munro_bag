// //menu icon
// function mainToggle(e) {
//     e.preventDefault();
//     document.getElementById("menuLinks").classList.toggle("open");
// }

//hide menu icon once clicked
const menuToggleBtn = document.getElementById("menuToggle");
if (menuToggleBtn) {
    menuToggleBtn.addEventListener("click", function (e) {
        e.preventDefault();

        const menu = document.getElementById("menuLinks");
        const icon = document.querySelector("#menuToggle svg");

        if (menu) {
            menu.classList.toggle("open");

            if (icon) {
                if (menu.classList.contains("open")) {
                    icon.classList.add("hidden");
                } else {
                    icon.classList.remove("hidden");
                }
            }
        }
    });
}


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
    const nav = document.querySelector('.nav-bar');
    const isHome = window.location.pathname === '/';
    const isMunros = window.location.pathname === '/munros/';

    if(nav && isHome){
        nav.style.fill = '#234473'
    } else if(nav && isMunros){
        nav.style.fill = '#4D86BB'
    } else {
        nav.style.fill = '#A3CAE1'
    }
}


window.addEventListener('DOMContentLoaded', () => {
    logoColour();
    // mountainTris();
    navColour();


    //add climb modal information
    var modal = document.getElementById("addClimb");
    var navModal = document.getElementById("menuLinks");
    var btn = document.getElementById("modalBtn");
    var nvBtn = document.getElementById("menuToggle");

    // Fix: Add Climb modal close button might not be the very first .close element on the page
    var climbModalCloseBtns = document.querySelectorAll("#addClimb .close");
    var navModalCloseBtn = document.querySelector("#menuLinks .close");

    if (btn) {
        btn.onclick = function(e){
            e.preventDefault();
            modal.style.display = "block";
            document.body.classList.add("modal-open");
        }
    }

    if (nvBtn) {
        nvBtn.onclick = function(){
            navModal.style.display = "block";
        }
    }

    if (climbModalCloseBtns.length > 0) {
        climbModalCloseBtns.forEach(function(closeBtn) {
            closeBtn.onclick = function(e){
                e.preventDefault();
                modal.style.display = 'none';
                document.body.classList.remove("modal-open");
            }
        });
    }

    // display chosen file name
    const actualBtn = document.querySelector('.photo-row input[type="file"]');
    const fileChosen = document.getElementById('file-chosen');

    if (actualBtn && fileChosen) {
        actualBtn.addEventListener('change', function(){
            if (this.files && this.files.length > 0) {
                if (this.files.length === 1) {
                    fileChosen.textContent = this.files[0].name;
                } else {
                    fileChosen.textContent = this.files.length + ' files chosen';
                }
            } else {
                fileChosen.textContent = 'No file chosen';
            }
        });
    }

    if (navModalCloseBtn) {
        navModalCloseBtn.onclick = function(){
            navModal.style.display = 'none';
        }
    }

    window.onclick = function(event){
        if (event.target == modal){
            modal.style.display = 'none';
            document.body.classList.remove("modal-open");
        }
    }


    //latest climb photos
    let currentPhoto = 0;
    const photos = document.querySelectorAll('.carousel-photo');

    function changePhoto(direction){
        photos[currentPhoto].style.display = 'none';
        currentPhoto = (currentPhoto + direction + photos.length) % photos.length;
        photos[currentPhoto].style.display = 'block';
    }

});
