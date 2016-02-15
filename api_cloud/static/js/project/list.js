/**
 * Created by yangjing on 2015/12/26.
 */
$(document).ready(function(){
    $(".btn-danger").click(function(){
        var confirm_info =confirm("确认删除？");
        if(confirm_info == true){
            var project_id = $(this).attr("id");
            project_id = project_id.substring(6);
            $.get("/api/project/del/",{project_id:project_id},function(result){
                 if(eval(result.heads).code == 0) {
                     window.location.href = "/api/project/list/";
                 }
                 else{
                     alert(eval(result.heads).message);
                 }
            });
        }

    });
});