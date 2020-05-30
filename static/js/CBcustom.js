function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#imgUpload')
                .attr('src', e.target.result);
        };

        reader.readAsDataURL(input.files[0]);
    }
}

index = 0
$('#btnSubmit').click(function(){

    var image = $('#imgUpload').attr('src');
    //console.log(image);
    var data = new FormData();
    data.append('image',image);

     $.ajax({
        type: 'POST',
        url: "/runBreedsCat",
        processData:false,
        contentType:false,
        data:data,
        success: function(predictions) {
            console.log(predictions);
            var div_result = $('#h3result');
            div_result.empty();
            var json = JSON.parse(predictions);
            var status = json['status'];
            if(status === 'nocat'){
                div_result.append("<div>No cat found in this image !</div>");
                return;
            }
            var predicts = json['predictions'];
            var index = 1;
            for(var pred in predicts)
            {
                var template =  '<div class="row">' +
                                '<div class="col-md-5">' +
								'	<img src="data:image/jpg;base64"' + '"{{pred[\'base64_encode\']}}" alt="img"></div>' +
								'<div class="col-md-3">' +
								'	<label>Giống: "{{pred[\'breed\']}}"</label></div>' +
								'<div class="col-md-2">' +
								'	<label>Tuổi: "{{pred["age"]}}"</label></div>' +
								'<div class="col-md-2">' +
								'	<label>Giới tính: "{{pred["gender"]}}"</label></div>';
                div_result.append(template);
            }
            div_result.append("<div>Thời gian thực hiện: '{{json[\"exetime\"}}'</div>");
            div_result.append("<div>Số lần chạy:" + index + "</div>");
            index += 1;
        },
        error: function(error){
            console.log(error);
            $('#divResult').empty().append("Có lỗi xảy ra");
            index += 1;
        }
    });
});


