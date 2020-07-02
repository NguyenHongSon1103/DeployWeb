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

var index = 1;
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
            var count = Number(json['count']);
            for(var i = 0; i < count; i++)
            {
                var pred = json['prediction_'+ i];
                var template =  '<div class="row">' +
                                    '<div class="col-md-5">' +
                                    '	<img src="data:image/jpeg;base64,' + pred['box'] + '" alt="img"></div>' +
                                    '<div class="col-md-7">' +
                                    '	<pre>Giống:' + pred["breed"] + '<br>' +
                                             'Tuổi:' + pred["age"] + '<br>' +
                                             'Giới tính:' + pred["gender"] +
                                        '</pre>' +
                                    '</div>' +
                                '</div>';
                div_result.append(template);
            }
            div_result.append("<div>Thời gian thực hiện:" + json["exetime"] + "</div>");
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


