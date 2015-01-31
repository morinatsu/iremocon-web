// auto_update.js
sensors_info_update = function(data){
    $("#illuminance").text(data.illuminance);
    $("#humidity").text(data.humidity);
    $("#temperature").text(data.temparature);
};
$(document).ready(function(){
    auto_update = function(){
        $.get("/api/auto_update",
            function(data){
                sensors_info_update(data);
            },
            "json"
        );
    };
    setInterval(auto_update, 180000);
});
