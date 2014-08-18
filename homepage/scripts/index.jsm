$(function(){
  $('#tiles .img-li').wookmark({
    autoResize: true, // This will auto-update the layout when the browser window is resized.
    container: $('#image-container'), // Optional, used for some extra CSS styling
    offset: 20, // Optional, the distance between grid items
    itemWidth: 250 // Optional, the width of a grid item
  });
});