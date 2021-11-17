var table = document.getElementsByClassName("table table-striped");
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);


window.onload = function(){loadfunction()}

function getCookie(cname){
  var name = cname + "=";
          var decodedCookie = decodeURIComponent(document.cookie);
          var ca = decodedCookie.split(';');
          for (var i = 0; i < ca.length; i++) 
              var c = ca[i];
              while (c.charAt(0) == ' ') 
                  c = c.substring(1);

              if (c.indexOf(name) == 0)
                  return c.substring(name.length, c.length);
          return "";
}

function loadfunction(){
  let names = document.getElementsByClassName("username");
  names[0].innerHTML = urlParams.get("username");

  let token = getCookie("token")

  $.ajax({
    url: "/api/v1/instructor/my_courses",
    type: "GET",
    contentType: 'application/json',
    data: payload
  }).done(function(response) {
    var json = JSON.parse(response)
    console.log(json)
  });
  }






