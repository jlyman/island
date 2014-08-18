 $(function() {
  // update the time every 1 seconds
  window.setInterval(function() {
    $('.browser-time').text('The current browser time is ' + new Date() + '.');
  }, ${ request.urlparams[1]});

  // update server time button
  $('#server-time-button').click(function() {
    $('.server-time').load('/homepage/index.gettime');
  });
});