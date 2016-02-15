/**
 * Created by yangjing on 2016/1/6.
 */
$(document).ready(function(){
    var project_id = $("#project_id").val();
    var selected_node_id = "";
    var selected_node_level = 0;
    function zTreeOnClick(event, treeId, treeNode) {
        selected_node_id = treeNode.id;
        selected_node_level = treeNode.level;
    };
    var setting = {
        check: {
		    enable: true,
		    chkStyle: "radio",
            radioType: "all"
	    },
        data: {
            simpleData:{
                enable:true,
                idKey: "id",
			    pIdKey: "pId",
			    rootPId: 0
            }
        },
        callback: {
		    onCheck: zTreeOnClick,
	    }
    };
    var treeNodes;

    $(function(){
        $.ajax({
            async : false,
            cache:false,
            type: 'POST',
            dataType : "json",
            data: {"project_id":project_id},
            url: "/api/project/tree/",//请求的action路径
            error: function () {//请求失败处理函数
                alert('请求失败');
            },
            success:function(data){ //请求成功后处理函数。
                treeNodes = data;   //把后台封装好的简单Json格式赋给treeNodes
            }
        });
        $.fn.zTree.init($("#project_parent_id"), setting, treeNodes);

    });
    $("#edit_project_save").click(function(){
        var project_name = $("#project_name").val();
        var api_document = $("#api_document").val();
        var project_level = selected_node_level+1;
        var parent_project_id = selected_node_id;
        $.post("/api/project/edit/",{project_id:project_id,project_level:project_level,parent_project_id:parent_project_id,
                                    project_name:project_name,api_document:api_document},function(result){
            if(eval(result.heads).code == 0)
            {
                alert("保存成功");
                opener.location.reload();
                window.location.reload();
            }
            else
            {
                alert(eval(result.heads).message);
            }
        });
    });
})