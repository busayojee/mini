const menu = document.querySelector('#mobile-menu');
const menuLinks = document.querySelector('.navbar ul');
menu.addEventListener('click',function() {
    menu.classList.toggle('is-active');
    menuLinks.classList.toggle('active')
});
window.navbar = function() {myFunction()};
function myFunction() {
    var x = document.getElementById('topnav');
    if (x.className === 'navbar'){
            x.className += 'responsive';
    }
    else{
        x.className = 'navbar';
    }
    
}
// When the user scrolls down 50px from the top of the document, resize the header's font size
window.onscroll = function() {scrollFunction()};
     
function scrollFunction() {
  if (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50) {
    document.getElementById("header").style.fontSize = "5px";
  } else {
    document.getElementById("header").style.fontSize = "15px";
  }
}


