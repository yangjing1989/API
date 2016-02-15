/**
 * Created by yangjing on 2015/12/25.
 */
$(document).ready(function(){
    var bodyHeight = ($(window).height())-80;
    $("#center").height(bodyHeight);
    $.get("/api/user/real/",function(result){
        $("#user_real_name").html("当前登录用户："+result);
    });
});