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
  let name_str = encodeURIComponent(String(username.value));
  let pass_str = encodeURIComponent(String(password.value));
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
  
  let payload = {"username":name_str, "password":pass_str}
  $.ajax({
    url: "/api/v1/auth/",
    type: "POST",
    contentType: 'application/json',
    data: payload
  }).done(function(response) {
    var json = JSON.parse(response)
    console.log(json)
    if (json.priveleges == "student")
    {
      window.location = "student_courses.html?username="+name_str
    }else if (json.priveleges == "instructor")
    {

      window.location = "teacher_courses.html?username="+name_str
    }else 
    {
      //window.location = "admin.html?username="+name_str
    }
  });

  
}
