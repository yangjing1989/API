/**
 * Created by yangjing on 2016/1/8.
 */
$(document).ready(function(){
    $("#edit_password_save").click(function(){
        var old_password = $("#old_password").val();
        var new_password = $("#new_password").val();
        var re_new_password = $("#re_new_password").val();
        $.post("/api/user/modify/",{old_password:old_password,new_password:new_password,re_new_password:re_new_password},function(result){
            if(eval(result.heads).code == 0) {
                alert("保存成功");
            }
            else{
                alert(eval(result.heads).message);
            }
        });
    });
});