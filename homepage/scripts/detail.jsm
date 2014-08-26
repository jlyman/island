$(function(){

  $('#start').off('click.add').on('click.add', function(evt) {
    var taskID = ${ request.urlparams[0] };
    $.ajax({
      url: '/homepage/task_ticket.create/' + taskID,
      success:function(result){
        $('#detail_instructions').html(result);
        $('#start').remove(); 
      },
    });

  });

  %if in_progress:
    $('#start').trigger('click.add');
  %endif

  $('#finish').off('click.add').on('click.add', function(evt) {
    $('#modal_load').loadmodal({
      url: '/product/add_to_cart/update/',
      id: 'custom_modal_id',
      title: 'Rate Task',
      width: '500px',
      ajax: {
        dataType: 'html',
        success: function(data, status, xhr) {
          console.log('hello');
        },
      },
    }); 
  });

});