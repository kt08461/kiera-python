function stopwatch() {
    // 開始
    var startTime = 0;
    var lapTime = 0;

    var now = function() {
        return (new Date().getTime());
    };
    
    this.span_text = function() {
        text = '<h3>圖片分析中...</h3>'
        text += '<span id="loading_time"></span>'
        return text
    };

    this.start = function() {
        //startTime = startTime ? startTime : now();
        startTime = now();
    };

    // 總共經歷的時間
    this.time = function() {
        return lapTime + (startTime ? now() - startTime : 0);
    };
}

function loading_time() {
    clocktimer = setInterval("update()", 1);
    t.start();
}

function update() {
    load_time.innerHTML = formatTime(t.time());
}

function pad(num) {
    return num < 10 ? '0'+num : num;
}

function formatTime(time) {
    var h = m = s = 0;
    // 停止的時間
    var newTime = ""
    
    //時
    h = Math.floor(time / (60 * 60 * 1000));
    time = time % (60 * 60 * 1000);
    
    // 分
    m = Math.floor(time / (60 * 1000));
    time = time % (60 * 1000);
    // 秒
    s = Math.floor(time / 1000);
    
    // 顯示時間計算結果，套用到幾位數格式上
    newTime = pad(h, 2) + ":" + pad(m, 2) + ":" + pad(s, 2);
    return newTime;
}

var t = new stopwatch();
var load_time

function resetbtn() {
    $("#uform")[0].reset();
    $(".cifar10_content").html('');
}

function imgCheck(img) {
    if (img !== undefined) {
        size = img.size / 1024 / 512
        if (size > 1) {
            alert("檔案大小已超過 512KB，請重新選擇")
            resetbtn();
            
            return false;
        } else {
            return true;
        }
    }
}

$("#upload_img").change(function (e) {
    img = e.target.files[0];
    imgCheck(img)
});

$("#btnSubmit").click(function () {
    fileinput = $("#upload_img")[0];
    img = fileinput.files[0];
    if (imgCheck(img)) {
        $(".cifar10_content").html( t.span_text() );
        load_time = document.getElementById("loading_time");
        loading_time();
        
        var formData = new FormData();           
        formData.append("upload_img", img);
        formData.append("csrfmiddlewaretoken", $("input[name=csrfmiddlewaretoken]").val());
        
        $.ajax({
            url: "/cifar10/",
            method: "Post",
            data: formData,
            cache: false,
            contentType: false,
            processData: false,
            success: function(response) {
                $(".cifar10_content").html(response);
            }
        });
    }
})

$("#btnReset").click(function (e) {
    resetbtn();
})
