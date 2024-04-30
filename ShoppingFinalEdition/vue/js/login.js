/**
 * 易购商城登录
 */
function login() {
  var username = document.getElementById("username");
  var pass = document.getElementById("password");
  console.log(username + "  " + pass);
  if (username.value == "") {
    alert("请输入用户名");
  } else if (pass.value == "") {
    alert("请输入密码");
  } else if (username.value == "admin" && pass.value == "123456") {
    /*  window.open("./index.html"); */
    window.location.href = "./index.html";
    window.event.returnValue = false;
  } else {
    alert("请输入正确的用户名和密码！");
  }
}
