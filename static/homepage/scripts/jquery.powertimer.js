(function($){$.fn.powerTimer=function(options,timerName){switch(options){case'stop':return funcStop.call(this,timerName);case'pause':return funcPause.call(this,timerName);case'continue':return funcContinue.call(this,timerName);case'options':return funcOptions.call(this,timerName);}
options=$.extend({func:null,params:{},name:TIMER_KEY,delay:-1,interval:-1,intervalAfter:-1,sleep:-1,sleepAfter:-1,stopAfter:-1,},options||{});funcStop.call(this,options.name);$(this).each(function(){setTimerValue(this,options.name,'options',options);setTimerValue(this,options.name,'starttime',new Date().getTime());funcContinue.call(this,options.name)});return this;};var funcStop=function(name){name=name||TIMER_KEY;$(this).each(function(){stopTimerByName(this,name);removeTimerValues(this,name);});return this;};var funcPause=function(name){name=name||TIMER_KEY;$(this).each(function(){stopTimerByName(this,name);setTimerValue(this,name,'timerid',false);});return this;};var funcContinue=function(name){name=name||TIMER_KEY;stopTimerByName(this,name);var options=getTimerValue(this,name,'options');if(options){$(this).each(function(){if(options.delay>=0){registerTimeout(this,options,options.delay);}else if(options.interval>=0){registerTimeout(this,options,options.interval);}else if(options.intervalAfter>=0){registerTimeout(this,options,0);}else if(options.sleep>=0){registerTimeout(this,options,options.sleep);}else if(options.sleepAfter>=0){registerTimeout(this,options,0);}});}
return this;};var funcOptions=function(name){return getTimerValue(this,name||TIMER_KEY,'options');};TIMER_KEY='jquery.powertimers.js';function registerTimeout(elem,options,duration){if(duration>0){setTimerValue(elem,options.name,'timerid',window.setTimeout(function(){callWithElement(elem,options);},duration));}else{setTimerValue(elem,options.name,'timerid','dummy');callWithElement(elem,options)}}
function callWithElement(elem,options){var now=new Date().getTime();if(options.stopAfter&&options.stopAfter>0&&now-getTimerValue(elem,options.name,'starttime')>options.stopAfter){$(elem).powerTimer('stop');return false;}
var ret=options.func.call(elem,options.params);stopTimerByName(elem,options.name);if(ret!==false&&options.delay<=0&&getTimerValue(elem,options.name,'timerid')){if(options.interval>=0){registerTimeout(elem,options,Math.max(0,options.interval-(new Date().getTime()-now)));}else if(options.intervalAfter>=0){registerTimeout(elem,options,Math.max(0,options.intervalAfter-(new Date().getTime()-now)));}else if(options.sleep>=0){registerTimeout(elem,options,options.sleep);}else if(options.sleepAfter>=0){registerTimeout(elem,options,options.sleepAfter);}}
return ret;}
function stopTimerByName(elem,name,clear){var timerid=getTimerValue(elem,name,'timerid');if(timerid){window.clearTimeout(timerid);}}
function getTimerValue(elem,name,key){var $elem=$(elem);if(!$elem.data(TIMER_KEY)){$elem.data(TIMER_KEY,[]);}
if(!$elem.data(TIMER_KEY)[name]){$elem.data(TIMER_KEY)[name]=[];}
return $elem.data(TIMER_KEY)[name][key];}
function setTimerValue(elem,name,key,value){getTimerValue(elem,name,key);$(elem).data(TIMER_KEY)[name][key]=value;}
function removeTimerValues(elem,name){getTimerValue(elem,name,'dummy');delete $(elem).data(TIMER_KEY)[name];}
var oldClean=jQuery.cleanData;$.cleanData=function(elems){for(var i=0,elem;(elem=elems[i])!==undefined;i++){$(elem).powerTimer('stop');}
return oldClean(elems);}})(jQuery);