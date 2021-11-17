var button = document.getElementById("submit")
var table = document.getElementsByClassName("table table-striped");
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);


window.onload = function(){loadfunction()}
button.onclick = function(){register_course()}

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

  let payload = {"username":names[0], "token":token, "spots_available":false}
  $.ajax({
    url: "/api/v1/student/all_courses",
    type: "GET",
    contentType: 'application/json',
    data: payload
  }).done(function(response) {
    var json = JSON.parse(response)
    console.log(json);
    var i = 0;
    json.forEach(element => {
      var row = document.createElement("TR");
      var text = text+"<td>"+json[i]["course_abbreviation"]+"<\\td>"
      text = text+ "<td>"+json[i]["course_name"]+"<\\td>"
      text = text+ "<td>"+json[i]["instructor"]+"<\\td>"
      text = text+ "<td>"+json[i]["time"]+"<\\td>"
      text = text+ "<td>"+json[i]["students_enrolled"]+"<\\td>"
      text = text+ "<td>"+json[i]["capacity"]+"<\\td>"
        row.appendChild(text);
      table[0].appendChild(row);
        i++
      })
    });
}

function register_course(){
  let names = document.getElementsByClassName("username");
  names[0].innerHTML = urlParams.get("username");
  let token = getCookie("auth-token")

  $('#rowclick2 tr').filter(':has(:checkbox:checked)').find('th').each(function() {
    // this = th element
  let payload = {"username":names[0], "token":token, "course_id":this.innerHTML}
  var course_id = this.innerHTML
  $.ajax({
    url: "/api/v1/student/register_course",
    type: "GET",
    contentType: 'application/json',
    data: payload
  }).done(function(response) {
    session = document.getElementById("session-result")
    var json = JSON.parse(response)
    console.log(json);
    var result = "";
      result = "<p>"+course_id+": "+json[i]["success"]+"<\\p> <br>"
    session.innerHTML = result
    i++
    });
  });
}





