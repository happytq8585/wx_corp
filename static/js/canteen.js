
$(function () {
        /*
    var dataArr = [{id:1,name:'凉拌三丝',title:'土豆、海带、细粉、蒜、葱、芥末',fraction:4.6,img:'img/97.jpg'},{id:2,name:'凉拌海带丝',title:'海带、蒜、葱、芥末',fraction:4.9,img:'img/97.jpg'}];
    var canteenList = '';
    dataArr.map(function (data,index) {
        console.log(data,index);
        canteenList += '<div class="canteenmenuBox">'+
            '<div class="left">'+
            '<a href="canteenList.html">'+
            '<img src='+data.img+' alt="">'+
            '</a>'+
            '</div>'+
            '<div class="left">'+
            '<p class="canteenmenuName">'+
            ' <span>'+data.name+'</span>'+
            '<span>'+data.fraction+'</span>'+
            ' </p>'+
            '<p> '+
            '<span>食材：</span>'+
            '<span class="canteenmenuMaterial">'+data.title+'</span>'+
            '</p>'+

        '<p> ' +
            '<div class="canteenmenuBtn" value='+data.id+' >立即预定</div>'+
            '</p>'+
            '</div>'+
            '<div class="clear"></div>' +
            '</div>'
    });
    $('.canteenLeft').append(canteenList);
    */
    
    $('.item-curMonth').click('on',function () {
        var datatime = $('.item-selected').attr('data');
         //日期数组【年，月，日】
        var dataarr = [datatime.substring(0,4),datatime.substring(4,6),datatime.substring(6)];

    });
    //打开预定弹窗
    var Reservenum ;
    $('.canteenmenuBtn').click('on',function () {
        console.log($(this).attr('value'));
        Reservenum = $(this).attr('value');
        $('.Reserve').css({display:'block'})
    })

    //关闭预定弹窗
    $('.ReserveClose').click('on',function(){
        $('.Reserve').css({display:'none'});
    })
    //确定预定弹窗
    $('.ReserveBtn').click('on',function () {
        $('.Reserve').css({display:'none'});
        // Reservenum  确定预定菜品的唯一值
        // $('.ReserveBox').find('input').val()  预定的数量

        console.log($('.ReserveBox').find('input').val());
    })

    
})
