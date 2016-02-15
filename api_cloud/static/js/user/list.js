/**
 * Created by yangjing on 2015/12/26.
 */
$(document).ready(function(){
    $(".btn-danger").click(function(){
        var confirm_info =confirm("确认删除？");
        if(confirm_info == true){
            var user_id = $(this).attr("id");
            user_id = user_id.substring(6);
            $.get("/api/user/del/",{user_id:user_id},function(result){
                 if(eval(result.heads).code == 0) {
                     window.location.href = "/api/user/list/";
                 }
                 else{
                     alert(eval(result.heads).message);
                 }
            });
        }

    });
});