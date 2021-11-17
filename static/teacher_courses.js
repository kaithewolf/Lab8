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
  let names = document.getElementsByClassName("bd-heading sticky-xl-top align-self-start mt-5 mb-3 mt-xl-0 mb-xl-2");
  names[0].innerHTML = "<h3>"+urlParams.get("username")+"</h3>";

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
    var i = 0;
    json.forEach(element => {
      var row = document.createElement("TR");
      var text = text+"<td>"+json[i]["course_abbreviation"]+"<\\td>"
      text = text+ "<td>"+json[i]["course_name"]+"<\\td>"
      text = text+ "<td>"+json[i]["time"]+"<\\td>"
      text = text+ "<td>"+json[i]["students_enrolled"]+"<\\td>"
      text = text+ "<td>"+json[i]["capacity"]+"<\\td>"
        row.appendChild(text);
      table[0].appendChild(row);
      i++
      })
  });
  }






