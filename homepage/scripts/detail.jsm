$(function(){

  String.prototype.toHHMMSS = function () {
    var sec_num = parseInt(this, 10); // don't forget the second param
    var hours   = Math.floor(sec_num / 3600);
    var minutes = Math.floor((sec_num - (hours * 3600)) / 60);
    var seconds = sec_num - (hours * 3600) - (minutes * 60);

    if (hours   < 10) {hours   = "0"+hours;}
    if (minutes < 10) {minutes = "0"+minutes;}
    if (seconds < 10) {seconds = "0"+seconds;}
    var time    = hours+':'+minutes+':'+seconds;
    return time;
}

  $('#start').off('click.add').on('click.add', function(evt) {
    var taskID = ${ request.urlparams[0] };
    $.ajax({
      url: '/homepage/task_ticket.create/' + taskID,
      success:function(result){
        $('#detail_instructions').html(result);
        $('#start').remove(); 
        var timing = $('#timing').attr("timevalue");
        console.log(timing);
        window.setInterval(function() {
          $('#timing').text(timing.toHHMMSS());
          timing = parseInt(timing);
          timing = timing + 1;
          timing = timing.toString();
        }, 1000);
    }});

  });

  %if in_progress:
    $('#start').trigger('click.add');
  %endif

});