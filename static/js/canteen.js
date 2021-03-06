function close_click()
{
    var id = $(this).attr('id');
    $.ajax({
            'Cookie': document.cookie,
            url:"/delete",
            type: "GET",
            data: {"id":id},
            success: function(para){
                alert("delete success");
                window.location.reload();
            },
            error: function(para) {
                alert("delete failed!");
                window.location.reload();
            }
    });
}
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
var DISHID=-1, DISHNAME="", IMGURL="";
function canteen_fill(day) {
    $.ajax({
        url: "/canteen",
        data: {"json":1, "day":day},
        type: "GET",
        success: function(para) {
            var arr = para.data;
            $('.canteenLeft').empty();
            for (var i = 0; i < arr.length; ++i) {
                var e   = arr[i];
                var loc = "/canteenItem?pic_src=" + e['pic_src'] + "&"               +
                          "dish_name=" + e['dish_name'] + "&"                        +
                          "average_score=" + e['average_score'] + "&"                +
                          "material=" + e['material'] + "&"                          +
                          "order=" + e['order'] + "&"                                +
                          "id=" + e['id'];
                var box = "<div class=\"canteenmenuBox\">"                           +
                              "<div class=\"left\">"                                 +
                                  "<a href=\"" + loc  + "\">"                        +
                   "<img src=\"" + e['pic_src'] + "\"" + " id=\"" + e['id'] + "\">"  +
                                  "</a>"                                             +
                              "</div>"                                               +
                              "<div class=\"left\">"                                 +
                                  "<p class=\"canteenmenuName\">"                    +
                                    "<span><h4>" + e['dish_name'] + "</h4></span>"   +
                                  "</p>"                                             +
                                  "<p>"                                              +
                                    "<span>食材: </span>"                            +
                                    "<span class=\canteenmenuMaterial\">"            +
                                          e['material'] + "</span>"                  +
                                  "</p>"                                             +
                                  "<p></p>"; 
                if (e['order'] == 1) {
                    box += "<div class=\"canteenmenuBtn\"" + "value=" +
                            e['id'] + ">立即预定</div>";
                }
                box +=                                                              
                            "<p></p>"                                                +
                              "</div>"                                               +
                              "<div class=\"right\">"                                +
                                "<img src=\"img/close.png\" class=\"img_close\""     +
                                    "id=\"" + e['id'] + "\"";
                if (para['role'] != 1) {
                    box +=  "hidden >";
                } else {
                    box +=  ">";
                }
                box += 
                              "</div>"                                               +
                              "<div class=\"clear\"></div>"                          +
                          "</div>";
                $('.canteenLeft').append(box);
            }
            $(".img_close").bind("click", close_click);
            $('.canteenmenuBtn').bind('click',function () {
                $('.Reserve').css({display:'block'});
                DISHID   = $(this).parent().children().eq(5).attr("value");
                DISHID   = parseInt(DISHID);
                DISHNAME = $(this).parent().children().eq(1).html();
                IMGURL   = $(this).parent().parent().children().first().children().children().attr("src");
            })
            if (para['role'] == 1) {
                var xsrf = get_cookie_by_name("_xsrf");
                var day  =  get_click_day();
                var form = 
                    "<form display=\"none\" class=\"form-horizontal\" role=\"form\" enctype=\"multipart/form-data\" method=\"post\" action=\"/up\">"                              +
                   // "{% raw xsrf_form_html() %}"                                       +
                "<div class=\"form-group\">"                                           +
                    "<div class=\"col-sm-10\">"                                        +
                    "<input type=\"hidden\" class=\"form-control\" name=\"day\"  value=\"" + day + "\">" +
                    "</div>"                                                           +
                "</div>"  +
                "<div class=\"form-group\">"                                           +
                    "<div class=\"col-sm-10\">"                                        +
                    "<input type=\"hidden\" class=\"form-control\" name=\"_xsrf\"  value=\""  + xsrf + "\">" +
                    "</div>"                                                           +
                "</div>"  +
                "<div class=\"form-group\">"                                           +
                    "<label for=\"dish_name\" class=\"col-sm-2 control-label\">菜名</label>"
                                                                                       +
                    "<div class=\"col-sm-10\">"                                        +
                    "<input type=\"text\" class=\"form-control\" name=\"dish_name\" placeholder=\"请输入名字\">"
                                                                                       +
                    "</div>"                                                           +
                 "</div>"                                                              +
                 "<div class=\"form-group\">"                                          +
                    "<label for=\"material\" class=\"col-sm-2 control-label\">食材</label>"
                                                                                       +
                    "<div class=\"col-sm-10\">"                                        +
                    "<input type=\"text\" class=\"form-control\" name=\"dish_material\" placeholder=\"请输入食材\">"
                                                                                       +
                    "</div>"                                                           +
                 "</div>"                                                              +
                 "<div class=\"form-group\">"                                          +
                    "<label for=\"picture\" class=\"col-sm-2 control-label\">图片</label>" 
                                                                                       +
                    "<div class=\"col-sm-10\">"                                        +
                    "<input type=\"file\" name=\"file\">"                              +
                    "</div>"                                                           +
                 "</div>"                                                              +
                 "<div class=\"form-group\">"                                          +
                    "<label for=\"choice\" class=\"col-sm-2 control-label\">是否可预订</label>"
                                                                                       +
                    "<div>"                                                            +
                    "<label class=\"radio-inline\">"                                   +
                    "<input type=\"radio\" name=\"dish_order\" id=\"optionsRadios3\" value=\"1\" checked>可以预订"                                                                +
                    "</label>"                                                         +
                    "<label class=\"radio-inline\">"                                   +
                    "<input type=\"radio\" name=\"dish_order\" id=\"optionsRadios3\" value=\"0\" value=\"option2\">不可以预订"
                                                                                       +
                    "</label>"                                                         +
                    "</div>"                                                           +
                 "</div>"                                                              +
                 "<div class=\"form-group\">"                                          +
                    "<div class=\"col-sm-offset-2 col-sm-10\">"                        +
                    "<input type=\"submit\" class=\"btn btn-default\">"                +
                    "</div>"                                                           +
                 "</div>"                                                              +
             "</form>";
                $('.canteenLeft').append(form);
            }
        }
    });
}
function get_click_day() {
    var datatime = $('.item-selected').attr('data');
     //日期数组【年，月，日】
    var d = [datatime.substring(0,4),datatime.substring(4,6),datatime.substring(6)];
    var day = d[0] + '-' + d[1] + '-' + d[2];
    return day;
}
function dayclick() {
    var day = get_click_day();
    canteen_fill(day);
}

$(function () {
    $('.item-curMonth').click('on',dayclick);
    $('.item-curDay').click('on', dayclick);
    $('.item-curDay').trigger('click');

    //打开预定弹窗
    var Reservenum ;
    $('.canteenmenuBtn').click('on',function () {
        $('.Reserve').css({display:'block'});
    })

    //关闭预定弹窗
    $('.ReserveClose').click('on',function(){
        $('.Reserve').css({display:'none'});
    })
    //确定预定弹窗
    $('.ReserveBtn').click('on',function () {
        $('.Reserve').css({display:'none'});
        var num = $('.ReserveBox').find('input').val(); // 预定的数量
        var dish_id = DISHID;
        var dish_name = DISHNAME;
        if (num == null || num < 1) {
            alert("预订数目不正确");
            return -1;
        }
        if (dish_id == null) {
            alert("菜的id不正确，无法预订");
            return -1;
        }
        if (dish_name == null) {
            alert("菜的名字不正确，无法预订");
            return -1;
        }
        var xsrf = get_cookie_by_name("_xsrf");
        if (xsrf == null) {
            alert("Missing parameter _xsrf");
            return -1;
        }
        var img_url = IMGURL;
        $.ajax({
            'Cookie': document.cookie,
            url: "/order",
            type: "POST",
            data: {"dish_id":dish_id, "num":parseInt(num), "dish_name":dish_name, "_xsrf":xsrf, "img_url": img_url},
            success: function(para) {
                alert(para);
            },
            error: function(para) {
                alert(para);
            }
        });
    });
    $(".img_close").bind("click", close_click);
})
