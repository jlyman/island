$(function() {
  
  /* Comment button at the top - moves focus down to the form */
  $('.post_comment_button').off('click.post_comment_button').on('click.post_comment_button', function() {
    $('#id_comment').focus();
  });//click
  
  /* Voting via ajax */
  $('.vote_up_link, .vote_down_link').off('click.vote_link').on('click.vote_link', function() {
    var link = $(this);
    $.ajax({
      url: '/forum/thread.vote/',
      data: {
        'id': link.attr('data-comment-id'),
        'vote': link.hasClass('vote_up_link') ? 'up' : 'down',
      },//data
      success: function(data) {
        link.closest('.voting_container').find('.current_vote').text(data);
      },//success
    });//ajax
  });//click
  
});