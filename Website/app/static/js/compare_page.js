$(document).ready(function() {
    $("#select_IP_button").click(function(){
        var ip = $("#select_IP").val();
        console.log(ip);
        var url = '/dash_board_2/'+ip
        $(location).attr('href',url);
    });
});


document.addEventListener("DOMContentLoaded", function(){
  function openTab(evt, tabName) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(tabName).style.display = "block";
  evt.currentTarget.className += " active";
}
document.getElementById("defaultOpen").click();
})

