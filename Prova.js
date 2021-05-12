
// Set the width of the sidebar to 250px and the left margin of the page content to 250px
/*
function openNav() {


  document.getElementById("mySidebar").style.width = "250px";
  //document.getElementById("main").style.marginLeft = "250px";
  document.getElementById("coso").style.marginLeft= "250px";
}
*/
// Set the width of the sidebar to 0 and the left margin of the page content to 0
/*
function closeNav() {
  document.getElementById("mySidebar").style.width = "0";
 //document.getElementById("main").style.marginLeft = "0";
  document.getElementById("coso").style.marginLeft= "0";

}
*/

function sidebar_open() {
  document.getElementById("mySidebar").style.width = "250px";
  document.getElementById("mySidebar").style.display = "block";
  document.getElementById("myOverlay").style.display = "block";
}

function sidebar_close() {
  document.getElementById("mySidebar").style.width = "0";
  document.getElementById("mySidebar").style.display = "none";
  document.getElementById("myOverlay").style.display = "none";
}
