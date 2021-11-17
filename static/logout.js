var username = document.getElementById("floatingInput")
var password = document.getElementById("floatingPassword")
var remember = document.getElementsByClassName("checkbox mb-3")
var button = document.getElementsByClassName("w-100 btn btn-lg btn-primary")
window.onload = function(){logout()}

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

function logout(){
  let token = getCookie("auth-token")
  window.location = "login.html"
  let payload = {"username":name_str, "token":token}
  $.ajax({
    url: "/api/v1/auth/logout",
    type: "POST",
    contentType: 'application/json',
    data: payload
  }).done(function(response) {
    var json = JSON.parse(response)
    console.log(json)
    if (json.success == true){
      window.location = "login.html"
    }
  });

  
}
