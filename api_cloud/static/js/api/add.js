/**
 * Created by yangjing on 2015/12/28.
 */
$(document).ready(function(){
    //加载期望结果
    var exp_txt = $("#expect_result_value_txt").val();
    if(exp_txt){
        try{
            $("#api_expect_result").JSONView(exp_txt);
        }
        catch(err){
            $("#api_expect_result").html(exp_txt);
        }
    }

    //选择form-data按钮时，显示参数列表
    $("#formdata_btn").click(function(){
        $('#body_btn button:not(this)').removeClass('active');
        $(this).addClass('active');
        $("#body_raw").hide();
        $("#body_url_data").hide();
        $("#body_form_data").show();
    });
    //选择url-data按钮时，显示参数列表
    $("#urlencoded_btn").click(function(){
        $('#body_btn button:not(this)').removeClass('active');
        $(this).addClass('active');
        $("#body_raw").hide();
        $("#body_form_data").hide();
        $("#body_url_data").show();
    });
    //选中raw按钮时，显示json输入框
    $("#raw_btn").click(function(){
        $('#body_btn button:not(this)').removeClass('active');
        $(this).addClass('active');
        $("#body_form_data").hide();
        $("#body_url_data").hide();
        $("#body_raw").show();
    });
    //选择POST请求方式时，显示请求体部分，否则隐藏
    show_post_body();
    $("#api_method").change(function(){
        show_post_body();
    });

    //参数输入框点击，生成新的参数行
    $("#url_params div input").click(function(){
        if($(this).val()==""){
            create_new_line("#url_params","api_params_key","Url Parameters Key","api_params_value","Value");
        }
    });
    //请求头输入框点击，生成新的请求头行
    $("#url_headers div input").click(function(){
        if($(this).val()==""){
           create_new_line("#url_headers","api_headers_key","Header","api_headers_value","Value");
        }
    });
    //body输入框点击，生成新的body行
    $("#body_form_data div input").click(function(){
        if($(this).val()==""){
           create_new_line("#body_form_data","body_form_key","Key","body_form_value","Value");
        }
    });
    //默认生成第一行参数
    create_new_line("#url_params","api_params_key","Url Parameters Key","api_params_value","Value");
    //默认生成第一行请求头
    create_new_line("#url_headers","api_headers_key","Header","api_headers_value","Value");
    //默认生成第一行body
    create_new_line("#body_form_data","body_form_key","Key","body_form_value","Value");
    //默认生成第一行body
    create_new_line("#body_url_data","body_url_key","Key","body_url_value","Value");

    //保存api信息
    $("#api_save_btn").click(function(){
        add_api_data("");
    });
    //保存修改
    $("#api_edit_save_btn").click(function(){
        var api_id = $("#api_id_txt").val();
        add_api_data(api_id);
    });

    //得到执行结果
    $("#api_execute_btn").click(function(){
            var api_id = $("#api_id_txt").val();
            var api_http_type = $("#api_http_type").val();
            var api_domain = $("#api_domain_txt").val();
            var api_url = $("#api_url_txt").val();
            var api_method = $("#api_method").val();
            var url_list = get_line_list("#url_params div","api_params_key","api_params_value");
            var api_headers = get_line_list("#url_headers div","api_headers_key","api_headers_value");
            var api_body_type = "";
            var api_body_value= "";
            if( api_method==2){
                if($("#formdata_btn").hasClass("active")){
                    api_body_type = 1;
                }
                else if($("#raw_btn").hasClass("active")){
                     api_body_type = 2;
                }
                else if($("#urlencoded_btn").hasClass("active")){
                     api_body_type = 3;
                }
                else{
                     api_body_type = "";
                }
                if(api_body_type == 1){
                    api_body_value=get_line_list("#body_form_data div","body_form_key","body_form_value");
                }
                else if(api_body_type == 3){
                    api_body_value=get_line_list("#body_url_data div","body_url_key","body_url_value");
                }
                else if(api_body_type==2){
                    api_body_value=$("#body_raw_data").val();
                }
                else{
                    api_body_value="";
                }
            }
            $.ajax({
        　　     url: "/api/api/result/",
             　　data:{api_id:api_id,api_http_type:api_http_type,api_url:api_url,url_list:url_list, api_domain:api_domain,api_method:api_method,api_headers:api_headers,api_body_type:api_body_type, api_body_value:api_body_value},
             　　type: "POST",
             　　dataType:'json',
             　　beforeSend: function(XMLHttpRequest){
                   $("#loading").html('<img src="/static/images/loading.gif">');
                 },
                 success: function(result){
                    if(eval(result.heads).code == 0)
                    {
                        var dataResult = eval(result.datas);
                        $("#api_real_result_no_form").text(dataResult);
                        try{
                            $("#api_real_result").JSONView(dataResult);
                        }
                        catch(err){
                            $("#api_real_result").html(dataResult);
                        }
                        var is_success = eval(result.heads).is_success;
                        if(is_success == 1){
                            $("#execute_result_txt").text("本次执行结果与预期一致，执行成功");
                            $("#execute_result_txt").removeClass("is_success_txt");
                        }
                        else if(is_success == 0){
                            $("#execute_result_txt").text("本次执行结果与预期不一致");
                            $("#execute_result_txt").addClass("not_same_txt");
                        }
                        else if(is_success == -1){
                            $("#execute_result_txt").text("执行失败，响应代码："+eval(result.heads).http_code);
                            $("#execute_result_txt").addClass("is_success_txt");
                        }
                    }
                    else if(eval(result.heads).code == 110000)
                    {
                        $("#api_real_result").html(eval(result.heads).exception);
                    }
                    else{
                        $("#api_real_result").html(eval(result.heads).message);
                    }
                 },
                 complete: function(XMLHttpRequest){
                    $("#loading").empty();
                 },
                 error : function(){
                    $("#loading").empty();
                 }
         });
    });

});
function show_post_body(){
    var request_method = $("#api_method").find("option:selected").text();
    if(request_method=="POST"){
            $("#post_body_div").show();
    }
    else{
            $("#post_body_div").hide();
    }
}

//生成新的行
function create_new_line(divid,key_name,key_place,value_name,value_place){
    var div = $("<div></div>");
    var input_key = $('<input name="'+key_name+'" type="text" placeholder="'+key_place+'" class="api_input">');
    var input_value = $('<input name="'+value_name+'" type="text" placeholder="'+value_place+'" class="api_input">');
    input_key.appendTo(div);
    input_key.click(function(){
        if($(this).val()==""){
            create_new_line(divid,key_name,key_place,value_name,value_place);
        }
    });
    input_value.appendTo(div);
    div.appendTo(divid);
}

//请求api的添加方法
function add_api_data(api_id){
    var expect_result = $("#api_real_result_no_form").text();
    var api_name = $("#api_name_txt").val();
    var api_http_type = $("#api_http_type").val();
    var api_domain = $("#api_domain_txt").val();
    var api_url = $("#api_url_txt").val();
    var api_method = $("#api_method").val();
    var project_id = $("#api_project_id").val();
    var api_remarks = $("#remarks_data").val();
    var url_list = get_line_list("#url_params div","api_params_key","api_params_value");
    var api_headers = get_line_list("#url_headers div","api_headers_key","api_headers_value");
    var api_body_type = "";
    var api_body_value= "";
    if( api_method==2){
        if($("#formdata_btn").hasClass("active")){
            api_body_type = 1;
        }
        else if($("#raw_btn").hasClass("active")){
             api_body_type = 2;
        }
        else if($("#urlencoded_btn").hasClass("active")){
            api_body_type = 3;
        }
        else{
             api_body_type = "";
        }
        if(api_body_type == 1){
            api_body_value=get_line_list("#body_form_data div","body_form_key","body_form_value");
        }
        else if(api_body_type==2){
            api_body_value=$("#body_raw_data").val();
        }
        else if(api_body_type==3){
            api_body_value=get_line_list("#body_url_data div","body_url_key","body_url_value");
        }
        else{
            api_body_value="";
        }
    }

    if(api_id==""){
        $.post("/api/api/add/",{api_name:api_name,project_id:project_id,api_http_type:api_http_type,api_url:api_url,url_list:url_list,
                            api_domain:api_domain,api_method:api_method,api_headers:api_headers,api_body_type:api_body_type,
                            api_body_value:api_body_value,api_result:expect_result,api_remarks:api_remarks},function(result){
            if(eval(result.heads).code == 0)
            {
                alert("保存成功");
                window.location.href = "/api/api/detail?api_id="+eval(result.api_id);
            }
            else
            {
                alert(eval(result.heads).message);
            }
        });
    }
    else{
        $.post("/api/api/edit/",{api_id:api_id,api_name:api_name,project_id:project_id,api_http_type:api_http_type,api_url:api_url,url_list:url_list,
                            api_domain:api_domain,api_method:api_method,api_headers:api_headers,api_body_type:api_body_type,
                            api_body_value:api_body_value,api_result:expect_result,api_remarks:api_remarks},function(result){
            if(eval(result.heads).code == 0)
            {
                alert("保存成功");
                window.location.reload();
            }
            else
            {
                alert(eval(result.heads).message);
            }
        });
    }

}
 function get_line_list(divid,keyname,valuename){
     var data_array = new Array();
     $(divid).each(function(){
         var bodykey = $(this).children("input[name='"+keyname+"']").val();
         var bodyvalue = $(this).children("input[name='"+valuename+"']").val();
         if(bodykey!=""&&bodyvalue!=""){
             var dataform = "{";
             dataform +='"'+bodykey+'":';
             dataform +='"'+bodyvalue+'"}';
             data_array.push(dataform);
         }
     });
     if( data_array.length>0)
     {
         var result = data_array.toString();
     }
     else
     {
         var result = "";
     }
     return result;
 }