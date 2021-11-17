username = document.getElementById("floatingInput")
password = document.getElementById("floatingPassword")
remember = document.getElementsByClassName("checkbox mb-3")
button = document.getElementsByClassName("w-100 btn btn-lg btn-primary")

remember.addEventListener('change', function() {
  if (this.checked) {
    console.log("Checkbox is checked..");
  } else {
    console.log("Checkbox is not checked..");
  }
});

button.onClick = function(){checkLogin()}

function checkLogin(){
  console.log(username.innerHTML);
  console.log(password.innerHTML);
}



console.log(username.innerHTML)