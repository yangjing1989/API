/**
 * Created by yangjing on 2016/1/7.
 */
$(document).ready(function(){
    var setting = {
        check: {
		    enable: true,
		    chkStyle: "checkbox",
            chkboxType: { "Y": "ps", "N": "ps" }
	    },
        data: {
            simpleData:{
                enable:true,
                idKey: "id",
			    pIdKey: "pId",
			    rootPId: 0
            }
        },
    };
    var treeNodes;
    $(function(){
        $.ajax({
            async : false,
            cache:false,
            type: 'POST',
            dataType : "json",
            url: "/api/project/user_tree/",//请求的action路径
            error: function () {//请求失败处理函数
                alert('请求失败');
            },
            success:function(data){ //请求成功后处理函数。
                treeNodes = data;   //把后台封装好的简单Json格式赋给treeNodes
            }
        });
        $.fn.zTree.init($("#user_permission"), setting, treeNodes);
    });

    $("#add_user_save").click(function(){
        var treeObj = $.fn.zTree.getZTreeObj("user_permission");
        var nodes = treeObj.getCheckedNodes(true);
        var permission_list = new Array();
        $.each(nodes, function(idx, obj) {
            permission_list.push(obj.id);
        });
        permission_list = permission_list.join(",");
        var user_name = $("#user_name").val();
        var user_real_name = $("#user_real_name").val();
        var user_password = $("#user_password").val();
        var user_re_password = $("#user_re_password").val();
        var user_email = $("#user_email").val();
        var is_admin = 0;
        if($('#is_admin').is(':checked')) {
            is_admin = 1;
        }
        else{
            is_admin = 0;
        }
        $.post('/api/user/add/',{user_name:user_name,user_real_name:user_real_name,
            user_password:user_password,user_re_password:user_re_password,user_email:user_email,
            user_is_admin:is_admin,permission_list:permission_list},function(result){
            if(eval(result.heads).code == 0) {
                alert("保存成功");
                opener.location.reload();
                window.location.reload();
            }
            else{
                alert(eval(result.heads).message);
            }
        });
    });
});