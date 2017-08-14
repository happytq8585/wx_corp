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
    $('.SurePassword').click('on',function () {
        var old = $("#old").val();
        var n1  = $("#new1").val();
        var n2  = $("#new2").val();
        if (old == null) {
            alert("旧密码不能为空");
            return -1;
        }
        if (n1 == null) {
            alert("新密码不能为空");
            return -1;
        }
        if (n1 == null) {
            alert("新密码确认不能为空");
            return -1;
        }
        if (n1 != n2) {
            alert("2次输入的新密码不正确");
            return -1;
        }
        var xsrf = get_cookie_by_name("_xsrf");
        $.ajax({
            'Cookie': document.cookie,
            url: '/personalcenter',
            type: "POST",
            data: {'old': old, 'passwd':n1, '_xsrf':xsrf, 'type': 1}, //type=1 rewrite password
            success: function(para) {
                alert("更新成功");
                window.location.reload();
            },
            error: function(para) {
                alert("更新失败");
                window.location.reload();
            }
        });
    });
    
})
