$(function() {
    $("#btn").on("click",function() {
        $.ajax({
            type: "POST",
            // url: "/ajax/",
            contentType: "application/json",
            dataType: "json",
            data: JSON.stringify(
                {"p1": $("#par1").val(),
                 "p2": $("#par2").val(),
                 "p3": $("#par3").val()
                }),
            success: function(response) {
                $('#out').text(response);
            }
        });
    });
});
