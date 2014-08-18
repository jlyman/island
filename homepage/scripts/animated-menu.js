$(function(){
//When mouse rolls over
$("li.animated").mouseover(function(){
$(this).stop().animate({height:'50px'},{queue:false, duration:600, easing: 'easeOutBounce'})
});

//When mouse is removed
$("li.animated").mouseout(function(){
$(this).stop().animate({height:'40px'},{queue:false, duration:600, easing: 'easeOutBounce'})
});
});