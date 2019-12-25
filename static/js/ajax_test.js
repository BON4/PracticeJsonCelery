$(document).ready(function () {
   $("#about-btn").click(function () {
       $.ajax({
           type: 'GET',
           async: true,
           url: 'task/',
          success: function (data) {
              $("#text-info").html(data['number']);
           },
           dataType: 'json',
       });
   });
});