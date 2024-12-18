/**
 * 易购商城注册
 */
function checkForm() {
  var nametip = checkUserName();
  var passtip = checkPassword();
  var conpasstip = ConfirmPassword();
  var phonetip = checkPhone();
  return nametip && passtip && conpasstip && phonetip;
}
//验证用户名
function checkUserName() {
  var username = document.getElementById("userName");
  var errname = document.getElementById("nameErr");
  var pattern = /^\w{3,12}$/; //用户名格式正则表达式：用户名要至少三位
  if (username.value.length == 0) {
    errname.innerHTML = "用户名不能为空";
    errname.className = "error";
    return false;
  }
  if (!pattern.test(username.value)) {
    errname.innerHTML = "用户名不合规范";
    errname.className = "error";
    return false;
  } else {
    errname.innerHTML = "OK";
    errname.className = "success";
    return true;
  }
}
//验证密码
function checkPassword() {
  var userpasswd = document.getElementById("userPasword");
  var errPasswd = document.getElementById("passwordErr");
  var pattern = /^\w{4,8}$/; //密码要在4-8位
  if (!pattern.test(userpasswd.value)) {
    errPasswd.innerHTML = "密码不合规范";
    errPasswd.className = "error";
    return false;
  } else {
    errPasswd.innerHTML = "OK";
    errPasswd.className = "success";
    return true;
  }
}
//确认密码
function ConfirmPassword() {
  var userpasswd = document.getElementById("userPasword");
  var userConPassword = document.getElementById("userConfirmPasword");
  var errConPasswd = document.getElementById("conPasswordErr");
  if (
    userpasswd.value != userConPassword.value ||
    userConPassword.value.length == 0
  ) {
    errConPasswd.innerHTML = "上下密码不一致";
    errConPasswd.className = "error";
    return false;
  } else {
    errConPasswd.innerHTML = "OK";
    errConPasswd.className = "success";
    return true;
  }
}
//验证手机号
function checkPhone() {
  var userphone = document.getElementById("userPhone");
  var phonrErr = document.getElementById("phoneErr");
  var pattern = /^1[34578]\d{9}$/; //验证手机号正则表达式
  if (!pattern.test(userphone.value)) {
    phonrErr.innerHTML = "手机号码不合规范";
    phonrErr.className = "error";
    return false;
  } else {
    phonrErr.innerHTML = "OK";
    phonrErr.className = "success";
    return true;
  }
}
//注册成功
function register() {
  if (checkForm()) {
    var r = confirm("注册成功是否跳转到登录页面");
    if (r == true) {
      /*  window.open("./index.html"); */
      window.location.href = "./index.html";
      window.event.returnValue = false;
    }
  } else {
    alert("信息有误");
  }
}
