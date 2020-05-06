index = 0
$('#btnSubmit').click(function(){
    var predict = '<div> {%= type %}<//div>'

    comment = $('textarea').val();
    var data = new FormData();
    data.append('comment',comment);

    console.log(comment);
     $.ajax({
        type: 'POST',
        url: "/runCommentSemantic",
        processData:false,
        contentType:false,
        data:data,
        success: function(predictions) {
            console.log(predictions);
             $('#divResult').empty();
            var type = JSON.parse(predictions)['prediction'];
            if(type == 1)
                meaning = 'Một câu mang ý nghĩa tốt !';
            else if (type == 0)
                meaning = 'Có một chút không tốt ở câu nói này !';
            else
                meaning = "Câu vừa nhập không có ý nghĩa";
             runtimes = 'Số lần thực hiện: '+ index
            $('#divResult').append('<h4> ' + runtimes + '</h4>');
            $('#divResult').append('<h3> ' + meaning + '</h3>');

            index += 1;
        },
        error: function(error){
            console.log(error);
            $('#divResult').empty();
            $('#divResult').append("Có lỗi xảy ra");
            index += 1;
        }
    });
});


