$(document).ready(function(){

    var csrf = $("input[name=csrfmiddlewaretoken]").val();

    $("#button11").click(function(){
        $.ajax({
            url: '',
            type: 'get',
            data: {
                "button_text" : $(this).text()
            },
            success: function(response){
                $("#button11").text(response.seconds) // adding it a new value
                $("#seconds").append('<li>' + response.seconds + '</li>')
            }
        })
    });


    $("#seconds").on('click', 'li', function(){
        $.ajax({
            url: '',
            type: 'post',
            data: {
                "text" : $(this).text(),
                'csrfmiddlewaretoken' : csrf
            },
            success: function(response){
                $("#down").append('<li> I wrote ' + response.text + '</li>')
            }
        })
    })
});