var table = document.getElementsByClassName("table table-striped");
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString); //username, classname, course_id


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
  let classname = document.getElementsByClassName("bd-heading sticky-xl-top align-self-start mt-5 mb-3 mt-xl-0 mb-xl-2");
  classname[0].innerHTML = "<h3>"+urlParams.get("classname")+"</h3>";


  let token = getCookie("auth-token")

  let payload = {"username":names[0], "token":token, "course_id":urlParams.get("course_id")}
  $.ajax({
    url: "/api/v1/instructor/course_students",
    type: "GET",
    contentType: 'application/json',
    data: payload
  }).done(function(response) {
    var json = JSON.parse(response)
    console.log(json)
  });
}





