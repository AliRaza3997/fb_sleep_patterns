let {PythonShell} = require('python-shell')
var path = require("path")
var bootstrap = require('bootstrap');
window.$ = window.jQuery = require('jquery')

function menuTabClicked(e) {
    console.log("button clicked: ", e);
}


$(document).ready(function() {

    $('#menuTabContainer > ul > li').on('click', function (e) {
      e.preventDefault()

      // Remove active class from all li elements
      $('#menuTabContainer > ul > li').removeClass('active')
       // Add active class to clicked li element
      $(this).addClass('active');


      // Find selector for clicked tab's content
      id = $(this).find("a").attr("href")
      tabContentSelector = "div".concat(id)

      $("#menuTabContainer > div > div").removeClass('active');
      $(tabContentSelector).addClass('active');

      console.log(tabContentSelector)
    })


    $("#myInput").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#friends-name-list > li").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });


})


function get_weather() {

  var city = document.getElementById("city").value
  
  var options = {
    scriptPath : path.join(__dirname, '/../engine/'),
    args : [city]
  }

  let pyshell = new PythonShell('weather_engine.py', options);


  pyshell.on('message', function(message) {
    swal(message);
  })
  document.getElementById("city").value = "";
}
