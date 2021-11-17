var username = document.getElementById("floatingInput")
var password = document.getElementById("floatingPassword")
var remember = document.getElementsByClassName("checkbox mb-3")
var button = document.getElementsByClassName("w-100 btn btn-lg btn-primary")


button.onClick = function(){checkLogin()}

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
    window.location = "student_courses.html"
  
}
