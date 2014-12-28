$(function() {
  // get the starter text into this namespace
  var starters = {};
  %for tid, encoded_starter in starters:
    starters['${ tid }'] = Base64.decode('${ encoded_starter }');
  %endfor

  // change event on the topic
  $('#id_topic > label').off('click.topic').on('click.topic', function() {
  	var editor = $('#id_comment').ckeditor().editor;
    var previous_label = $('#id_topic > label.active');
    var previous_starter = starters[previous_label.find('input').val()];
    if (editor.getData().trim() == previous_starter.trim() || editor.getData() == '') {
      // the previous starter is still there or it is empty, so we can add the new starter
      var new_label = $(this);
      var new_starter = starters[new_label.find('input').val()];
      editor.setData(new_starter);
    }//if
  });//click

});