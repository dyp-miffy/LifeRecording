const switchers = [...document.querySelectorAll('.switcher')];

switchers.forEach((item) => {
  item.addEventListener('click', function () {
    switchers.forEach((item) =>
      item.parentElement.classList.remove('is-active')
    );
    this.parentElement.classList.add('is-active');
  });
});


window.onload = function(){
  var msg=document.getElementById("msg").innerHTML;
  var denglu=document.getElementById("denglu");
  var zhuce=document.getElementById("zhuce");
  var msg1="密码输入不正确";
  var msg2="没登录请登录";
  var msg3="注册成功";
  if(msg==msg1||msg==msg2||msg==msg3){
      denglu.parentElement.classList.add('is-active');
      zhuce.parentElement.classList.remove('is-active');
  }

}
