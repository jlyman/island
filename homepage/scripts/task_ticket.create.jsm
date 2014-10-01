$(function() {
  

  function toHHMMSS(sec_num) {
//    var sec_num = parseInt(val, 10); // don't forget the second param
    var hours   = Math.floor(sec_num / 3600);
    var minutes = Math.floor((sec_num - (hours * 3600)) / 60);
    var seconds = Math.floor(sec_num - (hours * 3600) - (minutes * 60));

    if (hours   < 10) {hours   = "0"+hours;}
    if (minutes < 10) {minutes = "0"+minutes;}
    if (seconds < 10) {seconds = "0"+seconds;}
    var time    = hours+':'+minutes+':'+seconds;
    return time;
  }//toHHMMSS
  
  var page_load = new Date();
  
  $('#timing').powerTimer({
    intervalAfter: 1000,
    func: function() {
      var seconds_since_load = (new Date() - page_load) / 1000.0;
      var seconds_since_task_start = ${ timediff_at_page_load } + seconds_since_load;
      $(this).text(toHHMMSS(seconds_since_task_start));
    },
  });


  $('#finish').off('click.add').on('click.add', function(evt) {
    $.loadmodal({
      url: '/homepage/task_ticket.pre_finish/${ ticket.id }/',
      id: 'custom_modal_id',
      title: 'Rate Task',
      width: '500px',
    }); 
  });
  
});//ready