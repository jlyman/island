$(function(){

  $('#start').off('click.add').on('click.add', function(evt) {
    var taskID = ${ request.urlparams[0] };
    $.ajax({
      url: '/homepage/task_ticket.create/' + taskID,
      success:function(result){
        $('#detail_instructions').html(result);
        $('#start').remove();
    }});
  });

  %if in_progress:
    $('#start').trigger('click.add');
  %endif

});