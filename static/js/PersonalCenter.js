$(function () {
    $('.SurePassword').click('on',function () {
        $('.PersonalCenterBox').find('input').not('.SurePassword').map(function (index,data) {
            // console.log($(data).val(),index); 
            // $(data).val()  三次输入密码的数值   按顺序
        })
    })
})