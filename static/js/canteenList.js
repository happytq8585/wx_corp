function get_cookie_by_name(name)
{
    var start = document.cookie.indexOf(name);
    if (start != -1) {
        var res = "";
        var end  = document.cookie.indexOf(";", start+1);
        if (end == -1) {
            res = document.cookie.substring(start+name.length+1);
        } else {
            res = document.cookie.substring(start+name.length+1, end);
        }
        return res;
    }
    return "";
}
$(function () {

    var evaluatearr = [{id:1,username:'用户名',fraction:4.6,evaluate:'菜色很好，量也很足，很好',img:'img/username.png'},{id:2,username:'用户名2',fraction:4.7,evaluate:'菜色很好，量也很足',img:'img/username.png'}];
    var evaluateHtml = "";
    evaluatearr.map(function (data,index) {
        evaluateHtml+='<div class="canteenListEva">'+
            '<div class="left canteenListEvausername">'+
            '<img src='+data.img+' alt="">'+
            '<p>'+data.username+'</p>'+
            '</div>'+
            '<div class="left canteenListEvauserword">'+
            '<p>评分:<span>'+data.fraction+'</span></p>'+
            '<p>评论：<span>'+data.evaluate+'</span></p>'+
            '</div>'+
            '<div class="clear"></div>'+
            '</div>';
    })
    $('.canteenListBottom').append(evaluateHtml);

    //打开预定弹窗

    $('.canteenmenuBtn').click('on',function () {

        $('.Reserve').css({display:'block'})
    })

    //关闭预定弹窗
    $('.ReserveClose').click('on',function(){
        $('.Reserve').css({display:'none'});
    })
    //确定预定弹窗
    $('.ReserveBtn').click('on',function () {
        $('.Reserve').css({display:'none'});
        // $('.ReserveBox').find('input').val()  预定的数量
        console.log($('.ReserveBox').find('input').val());
    });


    //提交评论
    $('.UpdataBtn').click('on',function () {
        var star  = $('#rating').val();   //评论星星的数量；
        var words = $('#evaluate').val(); //评论文字的内容；
        $(".star").removeAttr("onMouseOver");
        $(".star").removeAttr("onMouseOut");
        $(".star").attr("href", "");
        var id = $("img").attr("id");
        var xsrf = get_cookie_by_name("_xsrf");
        $.ajax({
            'Cookie': document.cookie,
            url:"/comment",
            type: "GET",
            data: {"id":id, "star":parseInt(star), "words":words, "_xsrf":xsrf},
            success: function(para) {
                alert("comment success!");
                window.location.reload();
            }
        });
        //alert("OK");
    })



})
