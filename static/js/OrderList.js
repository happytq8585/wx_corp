$(function () {
    var Orderlist = [{id:1,name:'凉拌三丝',num:10,img:'img/97.jpg',time:'2017.7.4'},{id:2,name:'凉拌三丝',num:5,img:'img/97.jpg',time:'2017.7.14'},{id:3,name:'凉拌三丝',num:17,img:'img/97.jpg',time:'2017.7.9'}];
    var orderhtml = '';
    Orderlist.map(function (data,index) {
        orderhtml += '<div class="OrderListBoxCenter">'+
            '<img src='+data.img+' alt="">'+
            '<span>'+data.name+'</span>'+
            '<span>'+data.num+'份</span>'+
            '<span>'+data.time+'</span>'+
            '</div>'
        console.log(data,index);
    });
    
    $('.OrderListBox').append(orderhtml);

})