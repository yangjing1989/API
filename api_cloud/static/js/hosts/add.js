/**
 * Created by yangjing on 2015/12/26.
 */
$(document).ready(function(){
    $("#add_hosts_save").click(function(){
        hosts_name = $("#hosts_name").val();
        hosts_content = $("#hosts_content").val();
        $.post("/api/hosts/add/",{hosts_name:hosts_name,hosts_content:hosts_content},function(result){
            if(eval(result.heads).code == 0)
            {
                alert("保存成功");
                opener.location.reload();
                window.location.href = "/api/hosts/detail?hosts_id="+eval(result.hosts_id);
            }
            else
            {
                alert(eval(result.heads).message);
            }
        });
    });
});
