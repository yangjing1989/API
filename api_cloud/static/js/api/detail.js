/**
 * Created by yangjing on 2015/12/29.
 */
$(document).ready(function(){
    var default_url_list = $("#default_url_list").val();
    if(default_url_list!="")
    {
        default_url_list = default_url_list;
        var url_list = default_url_list.split(",");
        $.each(url_list,function(n,value){
            var obj = jQuery.parseJSON(value);
            for(var key in obj){
                load_default_line("#url_params","api_params_key","Url Parameters Key","api_params_value","Value",key,obj[key]);
            }
        });
    }


    var default_headers = $("#default_headers").val();
    if(default_headers!="")
    {
        default_headers = default_headers;
        var headers = default_headers.split(",");
        $.each(headers,function(n,value){
            var obj = jQuery.parseJSON(value);
            for(var key in obj){
                load_default_line("#url_headers","api_headers_key","Header","api_headers_value","Value",key,obj[key]);
            }
        });
    }

    var body_type = $("#body_type_txt").val();
    var default_body_value = $("#default_body_value").val();
    if(body_type==1 | body_type=="1"){
        $('#body_btn button:not(this)').removeClass('active');
        $("#formdata_btn").addClass('active');
        $("#body_raw").hide();
        $("#body_url_data").hide();
        $("#body_form_data").show();
        if(default_body_value!=""){
            default_body_value = default_body_value;
            var body_value = default_body_value.split(",");
            $.each(body_value,function(n,value){
                var obj = jQuery.parseJSON(value);
                for(var key in obj){
                    load_default_line("#body_form_data","body_form_key","Key","body_form_value","Value",key,obj[key]);
                }
            });
        }
    }
    else if(body_type==3 | body_type=="3"){
        $('#body_btn button:not(this)').removeClass('active');
        $("#urlencoded_btn").addClass('active');
        $("#body_raw").hide();
        $("#body_form_data").hide();
        $("#body_url_data").show();
        if(default_body_value!=""){
            default_body_value = default_body_value;
            var body_value = default_body_value.split(",");
            $.each(body_value,function(n,value){
                var obj = jQuery.parseJSON(value);
                for(var key in obj){
                    load_default_line("#body_url_data","body_url_key","Key","body_url_value","Value",key,obj[key]);
                }
            });
        }
    }
    else{
        $('#body_btn button:not(this)').removeClass('active');
        $("#raw_btn").addClass('active');
        $("#body_form_data").hide();
        $("#body_url_data").hide();
        $("#body_raw").show();
        $("#body_raw_data").val(default_body_value);
    }
});

function load_default_line(divid,key_name,key_place,value_name,value_place,keyvalue,valuevalue){
    var div = $("<div></div>");
    var input_key = $('<input name="'+key_name+'" type="text" placeholder="'+key_place+'" class="api_input" value="'+keyvalue+'">');
    var input_value = $('<input name="'+value_name+'" type="text" placeholder="'+value_place+'" class="api_input" value="'+valuevalue+'">');
    input_key.appendTo(div);
    input_key.click(function(){
        if($(this).val()==""){
            create_new_line(divid,key_name,key_place,value_name,value_place);
        }
    });
    input_value.appendTo(div);
    div.appendTo(divid);
}