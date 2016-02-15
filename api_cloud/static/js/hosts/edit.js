/**
 * Created by yangjing on 2015/12/26.
 */
$(document).ready(function(){
    $("#edit_hosts_save").click(function(){
        hosts_id = $("#hosts_id").val();
        hosts_name = $("#hosts_name").val();
        hosts_content = $("#hosts_content").val();
        $.post("/api/hosts/edit/",{hosts_id:hosts_id,hosts_name:hosts_name,hosts_content:hosts_content},function(result){
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
});
