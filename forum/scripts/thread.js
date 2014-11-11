$(function() {
  
  $('.post_comment_button').off('click.post_comment_button').on('click.post_comment_button', function() {
    $('#id_comment').focus();
  });//click
  
});