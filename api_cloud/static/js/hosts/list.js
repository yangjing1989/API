/**
 * Created by yangjing on 2015/12/26.
 */
$(document).ready(function(){
    $(".btn-danger").click(function(){
        var confirm_info =confirm("确认删除？");
        if(confirm_info == true){
            hosts_id = $(this).attr("id");
            hosts_id = hosts_id.substring(6);
            $.get("/api/hosts/del/",{hosts_id:hosts_id},function(result){
                 if(eval(result.heads).code == 0) {
                     window.location.href = "/api/hosts/list/";
                 }
                 else{
                     alert(eval(result.head).message);
                 }
            });
        }

    });
});