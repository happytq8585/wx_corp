
$(function () {
    //立即登录按钮事件以及判断
    $('.logBtn').click('on',function () {
        console.log($('.logname').val(),$('.logpass').val());
        var logname = $('.logname').val();
        var logpass = $('.logpass').val();
        if(logname==''&&logpass==''){
            $('.errorword').html('用户名，密码不能为空');
            $('.errorword').css({display:'block'});
        }else if(logname==''&&logpass!=''){
            $('.errorword').html('用户名不能为空');
            $('.errorword').css({display:'block'});
            console.log($('.errorword').val());
        }else if(logname!=''&&logpass==''){
            $('.errorword').html('密码不能为空');
            $('.errorword').css({display:'block'});
            console.log($('.errorword').val());
        }else{
            //将用户名，密码发送给后台经行验证，返回结果，判断是否正确
            
        }
    })


    $('.loginput').find('input').focus(function () {
        $('.errorword').css({display:'none'});
    })
})
