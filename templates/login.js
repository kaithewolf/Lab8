var username = document.getElementById("floatingInput")
var password = document.getElementById("floatingPassword")
var remember = document.getElementsByClassName("checkbox mb-3")
var button = document.getElementsByClassName("w-100 btn btn-lg btn-primary")


button.onClick = function(){checkLogin()}

window.onload = function(){getCookie(cname)}

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

function checkLogin(){
  let name_str = String(username.value)
  let pass_str = String(password.value)
  if (name_str == "" && pass_str == "")
  {
    alert("Missing username and password");
    return;
  }else if (name_str == "")
  {
    alert("Missing username");
    return;
  }else if (pass_str == ""){
    alert("Missing password");
    return;
  }

  //authenticate password
  //get user from databse
  //if (pass_str == user.password)
  //authenticate
  //if role is student, student_courses.html
  //if role is teacher, teacher_courses.html
  //if role is admin, admin.html
  window.location = "student_courses.html"
  
}
