$(function(){
  $(".classysocial").ClassySocial();  
});



//////////////////////////////////////////////////////////////
///   A generic 'loading' progress bar on the screen
///

$.meLoadingBar = {

  /* 
   * Shows the proress bar.  If name is provided, the progress bar will stay visible
   * until hide(name) is called, even if other calls to hide are run.
   */
  show: function(name, modal) {
    name = name || 'progress_bar_animation';
    var div = $('#progress_bar_animation');
    if (div.length == 0) {
      var img = '<img class="progress_bar_icon" src="/static/homepage/media/progress-bar-animation.gif" style="opacity: 0.0; position: fixed; left: 50%; top: 50%; margin-top: -10px; margin-left: -110px; z-index: 100002;"/>';
      if (!modal) {
        div = $('<div id="progress_bar_animation">' + img + '</div>');
      }else{
        div = $('<div id="progress_bar_animation" style="background-color: rgba(240, 240, 240, 0); position: fixed; height: 100%; width: 100%; z-index: 100001;">' + img + '</div>');
      }//if
      $('body').prepend(div);
      div.find('.progress_bar_icon').animate({ opacity: 0.9 }, 300);
    }//if
    
    // set the name in the progress bar names
    var name_array = div.data('progress_bar_names') || [];
    if ($.inArray(name, name_array) < 0) {
      name_array.push(name);
    }//if
    div.data('progress_bar_names', name_array);
  
    // return the name of the progress bar (generated or in parameters)
    return name;
  }, //show

  /* Returns true if the progress bar is showing */
  isShowing: function() {
    return $('#progress_bar_animation').length > 0;
  }, //isShowing

  /* 
   *  Removes the proress bar, unless other names are holding it visible.
   */
  hide: function(name) {
    var div = $('#progress_bar_animation');
    if (div.length > 0) {
      name = name || 'progress_bar_animation';
      var name_array = div.data('progress_bar_names') || [];
      var index = $.inArray(name, name_array);
      if (index >= 0) {
        name_array.splice(index, 1); // remove element
        div.data('progress_bar_names', name_array);
      }//if
      if (name_array.length == 0) {
        div.find('.progress_bar_icon').animate({ opacity: 0.0 }, 300, function() {
          div.remove();
        });
      }//if
    }//if
    return name;
  }, //hide
  
}//ProgressBar singleton object




/////////////////////////////////////////////////////
///   Our generic dialog boxes for the site

$.meDialog = {
  
  /**
   *   Loads a dialog from the server using Bootstrap's modal rather than the JQuery UI dialog above.
   *   This function requires the plugin at https://github.com/doconix/jquery.loadmodal.js.
   * 
   *   This function supports the changeover to Bootstrap's modal.
   *   Buttons should be placed in <div class="modal-footer"></div>
   *   Bootstrap automates the close behavior with <button data-dismiss="modal">
   */
  open: function(options) {
    // default options (feel free to override)
    options = $.extend(true, {
      url: null,                    // required
      id: 'island-dialog',      // use to style the dialog, if needed
      title: 'island',          // title for dialog
      width: '500px',
      idBody: null,                 // set below using the dialog id
      ajax: {                       // ajax parameters sent to JQuery.ajax
      },//ajax
      width: '400px',               // width of dialog in px or % (gets maxed at screen width)
      height: false,                // if set, height of the dialog in px or % (gets maxed at screen height)
      modal: {                      // modal options sent to Bootstrap.modal
        keyboard: false,            // don't allow esc key to close
        backdrop: 'static',         // don't allow clicking outside the dialog to close it
      },//modal
      buttons: {                    // set titles->functions to add buttons to the bottom of the dialog
      },//buttons 
    }, options);  
    if (options.idBody == null) {
      options.idBody = options.id + '_body';
    }//if
    
    // show the loading animation
    $.meLoadingBar.show();
    
    // maximize the width at the current window width, just in case we are on a very small screen
    if (String(options.width).indexOf('%') < 0) { // if not a percent
      var width = parseInt(options.width) || 500;
      options.width = Math.min(width, $(window).width()) + 'px';
    }//if
    
    // show a message to the user when we have a load error
    options.ajax.error = $.isArray(options.ajax.error) ? options.ajax.error : options.ajax.error ? [ options.ajax.error ] : [];
    options.ajax.error.unshift(function(xhr, status, msg) {
      $.meLoadingBar.hide();
      $.meDialog.topMessage('An error occurred loading the dialog from the server: ' + msg, 4000, 'danger');
    });//unshift error method
    
    // show a user message if an me-response-type header comes back with the response
    options.beforeShow = function(msg, status, xhr) {
      $.meLoadingBar.hide();
      if (xhr.getResponseHeader('me-response-type') != null) {
        if (xhr.getResponseHeader('me-response-type') == 'success') {
          $.meDialog.topMessage(msg, 4000, 'success');
        }else if (xhr.getResponseHeader('me-response-type') == 'warning') {
          $.meDialog.topMessage(msg, 4000, 'warning');
        }else {
          $.meDialog.topMessage(msg, 4000, 'danger');
        }//if
        return false; // returning false cancels the dialog from opening
      }//if
    };//beforeShow
  
    // remove the loading animation when the ajax completes
    options.ajax.success = $.isArray(options.ajax.success) ? options.ajax.success : options.ajax.success ? [ options.ajax.success ] : [];
    options.ajax.success.unshift(function() {
      $.meLoadingBar.hide();
    });//unshift success method

    // check the height of the dialog once it shows
    // we can't do this until the content loads into the modal and gets wrapped with the width
    options.onShow = function(dlg) {
      dlg.on('shown.bs.modal', function() {
        var dlgHeight = dlg.find('.modal-dialog').outerHeight(true) + 24; // +24 gives some padding on the bottom
        if (dlgHeight > $(window).height()) {
          var bodyHeight = dlg.find('.modal-body').outerHeight(true);
          dlg.find('.modal-body').height($(window).height() - (dlgHeight - bodyHeight));
        }//if
      });//show.bs.modal
    };//onShow
    
    // load the dialog
    $.loadmodal(options);
  },//open
  
  

  /** 
   *  Closes a dialog that was opened by $.meDialog.open2, if open. 
   *    dialog: a JQuery selector (typically to the #dialog_name used when opening the dialog),
   *            OR a JQuery object somewhere underneath the dialog,
   *            OR any DOM element within the dialog div itself, such as $.meDialog.close(this)
   */
  close: function(dialog, options) {
    // initialize the options
    options = $.extend({
      delay: 0,          // whether to delay the closing of the dialog
      reload: false,     // whether to reload the parent window of the dialog
    }, options);

    // get the dialog element and close it up
    elem = $(dialog).closest('.modal');
    if (elem.length > 0) {
      function closeNow() {
        elem.modal('hide');
//        elem.remove();
        if (options.reload) {
          window.location.reload();
        }//if
      }//closeIt

      // either delay the close or close now
      if (options.delay && options.delay > 0) {
        elem.powerTimer({
          delay: options.delay,
          func: closeNow,
        });//startTimer
      }else{
        closeNow();
      }//if
    }//if
  },//close


  /**
   *   Generic confirm dialog box with callbacks for each button.  The first button is set as the primary.
   *   Example: 
            $.meDialog.confirm('Title', 'Message', {
              Yes:           function(e) { alert('yes');   }, 
              No:            function(e) { alert('no');    },
              'Maybe Later': function(e) { alert('maybe'); },
            });
   *
   */
  confirm: function(title, message, buttons, width, modal_options) {
    // defaults
    width = width || 500;
    buttons = buttons || {};
    
    // options
    modal_options = $.extend(true, {
      keyboard: false,     // prevents closing by keyboard - we want to force a button click
      backdrop: 'static',  // prevents closing by clicking outside
      closeButton: false,  // whether to put a close X button at the top right
    }, modal_options);
    
    // set up the modal html
    var div = $([
                            '<div class="modal fade confirm-modal">',
                            '  <div class="modal-dialog modal-lg">',
                            '    <div class="modal-content">',
                            '      <div class="modal-header">',
modal_options.closeButton ? '        <button class="close" data-dismiss="modal" type="button">x</button>' : '',
                            '        <h4 class="modal-title">' + title + '</h4>',
                            '      </div>',
                            '      <div class="modal-body">',
                            '        <div class="modal-body-inner"></div>',
!$.isEmptyObject(buttons) ? '        <div class="modal-footer"></div>' : '',
                            '      </div>',
                            '    </div>',
                            '  </div>',
                            '</div>',
    ].join('\n'));
    div.find('.modal-body-inner').html(message);
    div.find('.modal-dialog').css('width', width);
    
    // add the buttons
    if (div.find('.modal-footer').length > 0) {
      var button_class = 'btn btn-primary';
      $.each(buttons, function(key, func) {
        var button = $('<button class="' + button_class + '">' + key + '</button>');
        div.find('.modal-footer').append(button);
        button.on('click.modal-footer', function(evt) {
          if (func) {
            func(evt);
          }//if
          div.modal('hide');
        });//click
        button_class = 'btn btn-default';  // only the first is the primary
      });//each
    }//if    
    
    // event to remove the content on close
    div.on('hidden.bs.modal', function (e) {
      div.remove();
    });//hidden.bs.modal
    
    // show the modal
    $('body').append(div);
    div.modal(modal_options);
    
  },//confirm function

  /**
   *   Yes/No dialog box
   *   Example: $.meDialog.yesno('Title', 'Message', function(e) { alert('yes'); }, function(e) { alert('no'); });
   *   The no function is optional
   */
  yesno: function(title, message, yes_callback, no_callback, width) {
    $.meDialog.confirm(title, message, {
      Yes: yes_callback,
      No: no_callback,
    }, width);
  },//yesno function

  /**
   *   Message dialog box
   *   Example: $.meDialog.message('Title', 'Message');
   */
  message: function(title, message, callback, width) {
    $.meDialog.confirm(title, message, {
      OK: callback,
    }, width, {
      backdrop: true,
      keyboard: true,
    });
  },//message function
  

  /**
   *   Message dialog box, but WITHOUT an OK button (just a close button at top and escape key active).
   *   Example: $.meDialog.message2('Title', 'Message');
   */
  message2: function(title, message, width) {
    $.meDialog.confirm(title, message, {}, width, {
      backdrop: true,
      keyboard: true,
      closeButton: true,
    });
  },//message function
  


  /**
   *   Input dialog box - get input from the user
   *   Example: $.meDialog.input('Title', 'Placeholder message', '6', function(e, val) { alert('The user entered ' + val); });
   *     If the user selects "cancel", the callback is sent val=undefined.
   */
  input: function(title, message, initial, callback, width) {
    // create the content with the input box
    var content = $([
      '<div class="input-container">',
      '<div class="input-message"></div>',
      '<div class="input-control"><input type="text" /></div>',
      '</div>',
    ].join('\n'));
    content.find('.input-message').html(message);
    if (initial != undefined) {
      content.find('.input-control').find('input').val(initial);
    }//if
    
    // call the confirm dialog with our content and the two buttons
    $.meDialog.confirm(title, content, {
      Submit: function(e) { 
        if (callback) {
          callback(e, content.find('.input-control').find('input').val());
        }//if
      },//submit func 
      Cancel: function(e) { 
        if (callback) {
          callback(e, undefined);
        }//if
      },//submit func 
    }, width);//confirm
    
    // set the focus on the input control
    $('.confirm-modal').on('shown.bs.modal', function() {
      $(this).find('.input-control').find('input').select();
    });
    
  },//input function



  /*
   *  Puts a message in a box at the top of the screen with a default 4 second duration.
   */
  topMessage: function(html, duration, type) {
    // add the html and get a reference to it
    var dlg = $('<div class="Dialogs_topMessage"></div>');
    dlg.hide();
    $('#header_message_center').append(dlg);
    type = typeof type == 'undefined' ? 'warning' : type;
    var msgType = "alert-"+ type;
    var alert = $('<div class="alert ' + msgType + '"></div>');
    alert.append('<button type="button" class="close" data-dismiss="alert">&times;</button>');
    alert.append(html)
    dlg.html(alert);
    dlg.fadeIn(600);
    // set a timer to remove it 
    duration = duration || 4000;
    dlg.powerTimer({
      delay: duration,
      func: function() {
        dlg.fadeOut(600, function() {
          dlg.remove();
        });
      }//func
    });//startTimer
    // return the new dialog
    return dlg;
  },//topMessage
  

} // Dialogs singleton object




/////////////////////////////////////////////////////////////////////////////////////////////////////
///   Customize the jQuery ajax call - adds a status bar
///
///   If you need  multiple progress bars, send "progressBarName" in the ajax call options, as in:
///     $.ajax({
///        ...
///        progressBarName: 'some name',
///        -- or --
///        progressBarName: false,  // to disable it
///     });
///
///   See the ProgressBar above for more detail on why names are useful.
///

$(function() {

  // Attach the progress bar to the JQuery ajax function (nice that jQuery comes with events to attach to).
  $(document).off('ajaxSend.island_custom').on('ajaxSend.island_custom', function(e, xhr, options) {
    if (options.progressBarName !== false) {
      options.progressBarName = $.meLoadingBar.show(options.progressBarName);
    }//if
    
  }).off('ajaxComplete.island_custom').on('ajaxComplete.island_custom', function(e, xhr, options) {
    if (options.progressBarName !== false) {
      $.meLoadingBar.hide(options.progressBarName);
    }//if
    
    // see if any topmessages came back - we automatically display these on ajax return - search the codebase for "HttpResponseWithHeaders" for use of this
    if (xhr.getResponseHeader('me_topmessage_success') != null) {
      $.meDialog.topMessage(xhr.getResponseHeader('me_topmessage_success'), 4000, 'success')
    }//if
    if (xhr.getResponseHeader('me_topmessage_warning') != null) {
      $.meDialog.topMessage(xhr.getResponseHeader('me_topmessage_warning'), 4000, 'warning')
    }//if
    if (xhr.getResponseHeader('me_topmessage_error') != null) {
      $.meDialog.topMessage(xhr.getResponseHeader('me_topmessage_error'), 4000, 'danger')
    }//if
  });//ajaxSend, ajaxComplete
  
});//ready



/////////////////////////////////////////////////////////////////////////////////////////////
///   Add a new JQuery method, nearly identical to $.load, but that replaces the given
///   element rather than loading beneath it.  This method is also optimized to run
///   as fast as possible, even though a large portion of the page might be replaced.
///
  
$(function() {

  jQuery.fn.loadReplace = function(url, data, callback) {
    return this.each(function() {
      
      // get the element
      var elem = $(this);
    
      // run the ajax
      $.ajax({
        url: url,
        type: 'POST',
        dataType: 'html',
        data: data,
        success: function(html, status, xhr) {
          // we detach all children first because removing an element with lots of children can take a LONG time.
          // this might be a memory management issue on a single-web-page app, but on our site people move page to page
          // so it isn't a problem to use a little more memory
          elem.children().each(function() {
            $(this).detach();
          });
          
          // now that the element is empty (the children are all detached from it), replace it with the new data
          elem.replaceWith(html);
          
          // call the callback, if there is one
          if (callback) {
            callback(this);
          }//if
    
        },//success
      
        error: function(xhr, status, errorStr) {
          $.meDialog.topMessage("An error occurred while loading data from the server: " + errorStr, 4000, "danger");
        },//error
      
      });//ajax
      
    	// allow chaining
    	return this;    
      
    });//each
  };//loadReplace
  
});//ready





