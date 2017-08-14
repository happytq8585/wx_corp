
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
    //传入的obj为本身的对象  x为该行的index值   从1开始
    function update(obj,x){
        var table = document.getElementById("table");
        for(var i=0;i<table.rows[x].cells.length-1;i++){
            var text = table.rows[x].cells[i].innerHTML;
            table.rows[x].cells[i].innerHTML = '<input class="input" name="input'+ x + '" type="text" value=""/>';
            var input = document.getElementsByName("input" + x);
            input[i].value = text;
            input[0].focus();
            input[0].select();
        }
        obj.innerHTML = "确定";
        obj.onclick = function onclick(event) {
            update_success(this,x);

        };
    }

    function update_success(obj,x, add){
        var arr = [];
        var table = document.getElementById("table");
        var input = document.getElementsByName("input" + x);
        for(var i=0;i<table.rows[x].cells.length-1;i++){
            var text = input[i].value;
            arr.push(text);
        }
        //把值赋值给表格，不能在取值的时候给，会打乱input的个数
        for(var j=0;j<arr.length;j++){
            table.rows[x].cells[j].innerHTML = arr[j];
        }
        //回到原来状态
        obj.innerHTML = "修改";
        obj.onclick = function onclick(event) {
            update(this,x)
        };

        //可在此处写ajax 传入修改的数据给后台  除了arr以外   还需要一个标记用户的属性
        var xsrf = get_cookie_by_name("_xsrf");
        //arr为修改后的用户名和密码
        var action = "action=update";
        var data_  = {'name': arr[0], 'passwd': arr[1], 'role': arr[2], 'uid':arr[3], '_xsrf': xsrf};
        if (add != null) {
            action = "action=add";
            data_ = {'name': arr[0], 'passwd': arr[1], 'role': arr[2], '_xsrf': xsrf};
        }
        $.ajax({
            'Cookie': document.cookie,
            url: '/employee?' + action,
            type: 'POST',
            data: data_,
            success: function(para) {
                if (add != null) {
                    alert("add success");
                } else {
                    alert("update success");
                }
                window.location.reload();
            },
            error: function(para) {
                alert("update failed");
                window.location.reload();
            }
        });
    }
    var UID = -1;
    //删除表格数据 可将x改为删除时所需要的数据
    function ondelete(obj,x){
        //console.log(obj,x);
        $('.Sure').css({display:'block'});

        UID = $('tr')[x].children[3].innerHTML;
        
    }
    //取消删除
    function surecancel(){
        $('.Sure').css({display:'none'});
    }
    //确认删除
    function suredelete(){
        if (UID == -1) {
            alert("UID==-1");
            return -1;
        }
        surecancel();
        var xsrf = get_cookie_by_name("_xsrf");
        $.ajax({
            'Cookie': document.cookie,
            url: '/employee?action=delete',
            type: 'POST',
            data: {'uid':UID, '_xsrf': xsrf},
            success: function(para) {
                alert("delete success");
                window.location.reload();
            },
            error: function(para) {
                alert("delete failed");
                window.location.reload();
            }
        });
        UID = -1;
    }

    //添加用户
    function add_username(){
        var num = $('.table1').find('tr').length;
        console.log(num);
        var innerhtml = '<tr>'+
            '<td>' +
            '<input class="input" name="input'+ num + '" type="text" value="用户名"/>' +
            '</td>'+
            '<td>' +
            '<input class="input" name="input'+ num + '" type="text" value="密码"/>' +
            '</td>'+
            '<td>' +
            '<input class="input" name="input'+ num + '" type="text" value="角色"/>' +
            '</td>'+
            '<td>'+
            '<button onclick="update_success(this,'+num+', 0)">确定</button>'+
            '<button onclick="adddelete()">删除</button>'+
            '</td>'+
            '</tr>';
        $('.table1').append(innerhtml);
    }


    //删除添加用户
    function adddelete(){
        //注意 添加的删除事件和已经存在的用户的删除事件  不一样
        $('.table1').find('tr').last().detach();
    }

