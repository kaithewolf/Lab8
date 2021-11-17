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

  let token = getCookie("auth-token")

  let payload = {"username":names[0], "token":token, "student_name":names[0]}
  $.ajax({
    url: "/api/v1/students/my_courses",
    type: "GET",
    contentType: 'application/json',
    data: payload
  }).done(function(response) {
    var json = JSON.parse(response)
    console.log(json)
  });
}





