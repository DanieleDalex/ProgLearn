function searchvideos(){
    $("#videos").empty();
    let text=document.getElementById("text").value;
    console.log(text);
    let temp = "https://youtube.googleapis.com/youtube/v3/search?part=snippet&q="+text+"&regionCode=US&type=video&videoCategoryId=27&key=AIzaSyBLci2d29vtfcPrr3NEkhwIFi0-6fK1rV4"
    console.log(temp);
    $.get(temp,function(data) {
        alert("success");
        console.log(data)
        data.items.forEach(item => {
        let tmp=`http://www.youtube.com/embed/${item.id.videoId}`
        console.log(tmp);
        $("#videos").append('<iframe id="videoid" src="'+tmp+'" allowFullScreen></iframe>');
    })})
    console.log(varr)
}

