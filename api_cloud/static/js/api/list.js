/**
 * Created by yangjing on 2015/12/29.
 */
$(document).ready(function(){
    var cur_page = 1;
    function zTreeOnClick(event, treeId, treeNode){
        $("#project_id_val").text(treeNode.id);
        project_click(treeNode.id,cur_page);
    }
    add_api_btn();
    //加载左侧项目树
    load_tree(zTreeOnClick,"#project_tree");
    //批量移动
    batch_move();
    //批量删除
    batch_del();
    //批量执行
    batch_exe();
    //刷新
    refresh();

});
function load_tree(callback_fn,tree_div_id){
    var user_id = $("#uid_value").text();
    var setting = {
        check: {
		    enable: false,
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
		    onClick: callback_fn
        }
    };
    var treeNodes;
    $(function(){
        $.ajax({
            async : false,
            cache:false,
            type: 'POST',
            dataType : "json",
            data:{user_id:user_id},
            url: "/api/project/per_tree/",//请求的action路径
            error: function () {//请求失败处理函数
                alert('请求失败');
            },
            success:function(data){ //请求成功后处理函数。
                treeNodes = data;   //把后台封装好的简单Json格式赋给treeNodes
            }
        });
        $.fn.zTree.init($(tree_div_id), setting, treeNodes);
    });
}
function project_click(project_id,cur_page){
    $("#exe_result").hide();
    $.get("/api/api/data/",{project_id:project_id,page:cur_page},function(result){
            create_table_data(eval(result).data);
            $("#data_counts").text("总共："+eval(result).counts+"条记录，");
            $("#page_counts").text("共："+eval(result).pages+"页");
            create_page(cur_page, eval(result).pages);
            $("#next_page").click(function(){
                if(cur_page<eval(result).pages){
                    cur_page = cur_page+1;
                    $("#cur_page").text(cur_page+"/"+eval(result).pages);
                    $.get("/api/api/data/",{project_id:project_id,page:cur_page},function(result){
                        create_table_data(eval(result).data);
                    });
                }
            });
            $("#pre_page").click(function(){
                if(cur_page>1){
                    cur_page = cur_page-1;
                    $("#cur_page").text(cur_page+"/"+eval(result).pages);
                    $.get("/api/api/data/",{project_id:project_id,page:cur_page},function(result){
                        create_table_data(eval(result).data);
                    });
                }
            });
        });
}

function create_table_data(data_obj){
    $("#api_list").empty("");
    var thead = $("<thead></thead>");
    var first_tr = $("<tr></tr>");
    $('<th><input type="checkbox" id="select_all_apis"></th> <th>ID</th> <th>接口名称</th> <th>域名</th>').appendTo(first_tr);
    $('<th>Url</th> <th>Method</th> <th>创建人</th> <th>是否执行成功</th>').appendTo(first_tr);
    first_tr.appendTo(thead);
    thead.appendTo("#api_list");
    $.each(data_obj, function(i, item) {
        var tr = $("<tr></tr>");
        $('<td><input type="checkbox" id="api'+item.id+'" name="api_check"></td>').appendTo(tr);
        $("<td>"+item.id+"</td>").appendTo(tr);
        $("<td><a target='_blank' href='/api/api/detail/?api_id="+item.id+"'>"+item.name+"</a></td>").appendTo(tr);
        $("<td>"+item.api_domain+"</td>").appendTo(tr);
        $("<td>"+item.api_url+"</td>").appendTo(tr);
        $("<td>"+item.api_method+"</td>").appendTo(tr);
        $("<td>"+item.creater+"</td>").appendTo(tr);
        if(item.api_is_success == 1){
            $("<td style='color:green;'>成功</td>").appendTo(tr);
        }
        else if(item.api_is_success == 0){
            $("<td style='color:#cf910b;'>与上次执行结果不一致</td>").appendTo(tr);
        }
        else if(item.api_is_success == -1){
            $("<td style='color:red;'>失败</td>").appendTo(tr);
        }
        else{
            $("<td></td>").appendTo(tr);
        }
        tr.appendTo("#api_list");
    });
    //单选，全选
    $("#select_all_apis").click(function(){
        if($("#select_all_apis").attr("checked"))
        {
            $("#select_all_apis").removeAttr("checked");
            $("[name='api_check']").removeAttr("checked");
        }
        else{
            $("#select_all_apis").prop("checked",true);
            $("[name='api_check']").prop("checked",true);
            $("#select_all_apis").attr("checked",true);
            $("[name='api_check']").attr("checked",true);
        }
    });

    $("[name='api_check']").click(function(){
        if($(this).attr("checked")){
            $(this).removeAttr("checked");
        }
        else
        {
             $(this).prop("checked",true);
             $(this).attr("checked",true);
        }
    });
}

function create_page(cur_page, pages){
    $("#show_data_page").empty("");
    var ul = $('<ul class="pagination"></ul>');
    var pre_page = $('<li><a href="#" id="pre_page">&laquo;</a></li>');
    var cur_page = $('<li><a href="#" id="cur_page">'+cur_page+'/'+pages+'</a></li>');
    var next_page = $('<li><a href="#" id="next_page">&raquo;</a></li>');
    pre_page.appendTo(ul);
    cur_page.appendTo(ul);
    next_page.appendTo(ul);
    ul.appendTo("#show_data_page");
}

function batch_del(){
   //批量删除
    $("#batch_del_btn").click(function(){
        var api_list = get_selected_list();
        if(api_list.length<1){
            alert("请选择要删除的接口");
        }
        else{
            var confirm_info =confirm("确认删除？");
            if(confirm_info == true){

                $.post("/api/api/del/",{api_list:api_list},function(result){
                  if(eval(result.heads).code == 0)
                  {
                      project_click($("#project_id_val").text(),1);
                  }
                  else
                   {
                     alert(eval(result.heads).message);
                   }
                });
            }
        }
    });
}

function batch_exe(){
    //批量执行
    $("#batch_exe_btn").click(function(){
        $("#exe_result").hide();
        $("#exe_result_txt").empty("");
        var api_list = get_selected_list();
        if(api_list.length<1){
            alert("请选择要执行的接口");
        }
        else{
            $.ajax({
                type: 'POST',
                url:"/api/api/batch/",
                data:{api_list:api_list},
                beforeSend: function(XMLHttpRequest){
                    $("#loading").html('<img src="/static/images/loading.gif">');
                },
                success: function(result){
                    var show_page = $("#cur_page").text().split("/")[0]
                    project_click($("#project_id_val").text(),parseInt(show_page));
                    $("#exe_result").show();
                    $("#exe_result_txt").text("失败："+eval(result).failed_count+"条，不一致："+eval(result).not_same+"条，成功："+eval(result).success_count+"条");
                },
                complete: function(XMLHttpRequest){
                    $("#loading").empty();
                },
                error : function(){
                    $("#loading").empty();
                }
            });
        }

    });
}

function batch_move(){
    //批量移动
    $("#batch_move_btn").click(function(){
        load_tree("","#show_all_project");
    });
    $("#save_move_btn").click(function(){
        var api_list = get_selected_list();
        var treeObj = $.fn.zTree.getZTreeObj("show_all_project");
        var nodes = treeObj.getSelectedNodes();
        if(api_list.length<1){
            alert("请选择要移动的接口");}
        else{
           if(nodes.length>1){
            alert("只能选择一个项目");
            }
            else if(nodes.length<1){
                alert("请选择要移动到的项目");
            }
            else{
                var move_to_project = nodes[0].id;
                $.post("/api/api/move/",{api_list:api_list,project_id:move_to_project},function(result){
                    if(eval(result.heads).code == 0) {
                        alert("保存成功");
                        $("#move_api").hide();
                        project_click($("#project_id_val").text(),1);
                    }
                    else{
                        alert(eval(result.heads).message);
                    }
                });
            }
        }

    });
}

function get_selected_list(){
    var api_list = [];
    $("[name='api_check'][checked='checked']").each(function(){
            var api_id = $(this).attr("id");
            api_id = api_id.substring(3);
            api_list.push(api_id);
    });
    api_list = api_list.join(",");
    return api_list;
}

function refresh(){
    $("#refresh_btn").click(function(){
        var project_id = $("#project_id_val").text();
        if(project_id==""){
            window.location.reload();
        }
        else{
            project_click(parseInt(project_id),1);
        }
    });
}

function add_api_btn(){
    $("#new_api_btn").click(function(){
        var project_id = $("#project_id_val").text();
        var api_list = get_selected_list();
        if(api_list.length>=1)
        {
            window.open("/api/api/new/?api_id="+api_list.split(",")[0]);
        }
        else if(api_list.length<1&&project_id!=""){
            window.open("/api/api/new/?project_id="+parseInt(project_id));
        }
    });
}