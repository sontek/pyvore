$(document).ready(function() {
    var socket = io.connect();
//   var socket = new io.Socket(null, {});

    socket.on("connect", function () {
        // we are connected... nothing to do really
    });

    socket.on("message", function () {
        // we are going to use custom messages, no reason to have this
    });

    socket.on("chat", function (e) {
        $("#chatlog").append(e + "<br />");
    });

    socket.on("disconnect", function () {
        // socket disconnected
    });

    $("#submit").click(function() {
        var val = $("#chatbox").val();
        socket.emit("chat", val);
        $("#chatbox").val("");
    });
});
