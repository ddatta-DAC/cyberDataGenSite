$(document).ready(function() {
    $("#select_IP_button").click(function(){
        var ip = $("#select_IP").val();
        console.log(ip);
        alert("The paragraph was clicked." +ip);
        var url = '/dash_board_2/'+ip
        $(location).attr('href',url);
    });
});
