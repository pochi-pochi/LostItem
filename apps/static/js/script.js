// Webカメラから映像を取得する
// if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
//     navigator.mediaDevices.getUserMedia({ video: true }).then(function (stream) {
//         document.getElementById('video').srcObject = stream;
//     });
// }

navigator.mediaDevices.getUserMedia({ video: true }).then(function (stream) {
    var video = document.getElementById("my-video");

    video.addEventListener("click", function () {
        // 動画をキャプチャする
        var canvas = document.createElement("canvas");
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        var ctx = canvas.getContext("2d");
        ctx.drawImage(video, 0, 0);

        // 動画を保存する
        var image = canvas.toDataURL("image/jpg");
        var link = document.createElement("a");
        link.download = "captured-video.jpg";
        link.href = image;
        link.click();
    });


    video.srcObject = stream;
});

