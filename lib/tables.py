from django import forms
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseRedirect, Http404
import mako.runtime
from lib.filters import *
from . import flat_attr
import collections, json, math



###################################################################
###   The bootstrapped paginated version of our table.
###   This table is the primary table we use.  It paginates
###   AND filters on the client side using Javascript.
###
###   To repaginate the table (suppose you modify it with JS):
###     $('div.your_css_class').trigger('customtable_paginate');
###
###   To filter the table, first set a handler function that will test each <tr>:
###     $('div.your_css_class').off('customtable_filter.some_unique_name').on('customtable_filter.some_unique_name', function(event) {
###       if (!event.filtered) { // has another handler already filtered this record?
###         event.filtered = some boolean test; // $(event.row) or "event.row" is the current <tr> being tested
###       }//if
###     });//customtable_filter
###   Then trigger the table filtering with:
###     $('div.your_css_class').trigger('customtable_run_filter');
###   Running the filter automatically updates the pagination links.
###   The handler function is attached to the table div rather than individual rows so it only has to attach to one element rather than many.
###


class TableRow(list):
  '''A row in the table.  Use this instead of a regular list if you need to add parameters like css to the <tr>.'''
  def __init__(self, row_data, css_class=''):
    '''Constructor''' 
    list.__init__(self, row_data)  # the new super() way of doing things didn't work here.  not sure why.
    self.css_class = css_class
    
    
class TableCell(object):
  '''A table cell in the table.  Use this when you need to add parameters like css to the <td>'''
  def __init__(self, value, css_class=None, attrs=None):
    self.value = value
    self.css_class = css_class  # if included, added to the class="..." of the <td>
    self.attrs = attrs          # if a dict, adds attributes to the <td>
    
  def __str__(self):
    return str(self.value)
    
  def __bytes__(self):
    return str(self.value).encode('utf8')


class TableHeader(object):
  '''A header for the custom table.
       title         = The title to show in the <th> of this column.
       
       Formatting: there are several ways to format the column; these can be used separately or together:
       css_class     = A css class to give every <th> and <td> in this column.
       formatter     = A python string format to use when outputting the html.  For example, '%.2f' will give the value in this column two decimal places.
                       If you use a number format like '%.2f', the value in the cell should be a float.
       cell_viewer   = A def name that lazy-renders the cell.  The def MUST be defined at the top-level of a template, not within a block or other def.
                       This option is the most complex and powerful way to format the cell because you can use a Mako def.  Search for examples of 
                       'cell_viewer' in our code for how to do it.
  '''
  def __init__(self, title, css_class='', formatter=None, format_func=None, cell_viewer=None, sortable=True, query_order_by_name=None, query_order_by_case_insensitive=False):
    self.title = title
    self.css_class = css_class
    self.formatter = formatter
    self.cell_viewer = cell_viewer
    self.sortable = sortable
    self.query_order_by_name = query_order_by_name  # for ServerSideTables, this gives the name to use in order_by
    self.query_order_by_case_insensitive = query_order_by_case_insensitive  # again for ServerSideTables

    

class ClientSideTable(list):
  '''Our custom, sortable table.  This is the table we use throughout the site.'''
  headings = [ 
    TableHeader('Column 1', 'customtable_col1'), 
    TableHeader('Column 2', 'customtable_col2'), 
    TableHeader('Column 3', 'customtable_col3'), 
  ]
  sortable = True            # set to false to disable sorting
  show_headings = True       # whether to show the headings or not
  rows_per_page = 0          # the number of rows per page to show (0 means no pagination)
  table_attrs = {}           # additional name=value pairs on the <table> element
  filter_controls_selector = '#customtable_filter_container'  # the div that contains the filter controls
  title = None
  # subclasses add with css_class = ClientSideTable.css_class + ' whatever'
  css_class = 'customtable table tablesorter table-striped table-hover'   
  # subclasses add with row_css_class = ClientSideTable.row_css_class + ' whatever'
  # you can also add with special TableRow class.
  # note that some JS below depends on rows having the customtable_row class.
  row_css_class = 'customtable_row'   
  # where to place the pagination links
  pagination_links_top = True
  pagination_links_bottom = True
  

  def __init__(self, request, *args, **kwargs):
    '''Constructor'''
    super().__init__(*args, **kwargs)
    self.request = request
    self.guid = request.generate_webid()


  def __str__(self):
    '''Returns the html for this table'''
    return self.as_table()
    
    
  def get_html(self, context=None):
    '''Returns the html for this table. If a cell_viewer was specified in a header, the call should include the calling context.'''
    return self.as_table(context)
    
    
  def as_table(self, context=None):
    '''Returns the html for this table using <table> tags (this is the normal way)'''
    html = []
    
    # set up the cell viewers, if there are any
    cell_viewers = self._get_cell_viewers(context)

    # header
    html.append('''<div id="%s" class="%s">''' % (self.guid, self.css_class))

    # scripts for behavior
    if self.pagination_links_top:
      self._add_pagination_html(html, True)

    # table start
    html.append('''<table id="table_%s" class="%s" %s>''' % (self.guid, self.css_class, ' '.join(['%s="%s"' % (k, v) for k, v in list(self.table_attrs.items()) ])))
    
    # table header row
    if self.show_headings:
      html.append('''<thead>''')
      html.append('''  <tr class="%s">''' % self.row_css_class)

      if self.title:
        html.append('''  <th colspan="%s" class="title">%s</th>''' % (len(self.headings), self.title))
        html.append('''</tr>''')
                    
      for i, heading in enumerate(self.headings):
        if isinstance(heading, TableHeader):
          html.append('''  <th class="customtable_header %s %s">%s</th>''' % (heading.css_class, 'tablesorter' if self.sortable and heading.sortable else '', heading.title))
        else:
          html.append('''  <th class="customtable_header tablesorter">%s</th>''' % (heading))

      html.append('''  </tr>''')
      html.append('''</thead>''')

    # add the table rows
    html.append('''  <tbody>''')
    for row in self:
      self._add_table_row(context, html, row, cell_viewers, row_tag='tr', cell_tag='td')
    html.append('''  </tbody>''')
      
    # table end
    html.append('''</table>''')
    
    # scripts for behavior
    self._add_extra_html(html)
    self._add_sorter_html(html)
    self._add_filter_html(html)
    if self.pagination_links_bottom:
      self._add_pagination_html(html, False)
    
    # footer
    html.append('</div>')
    
    # return the html
    return ''.join(html)
  
    
  def as_table_row(self, row, context=None):
    '''Gets a single table row.  This method is provided for times when only a single row needs to be printed, such
       as an ajax replace of a table row'''
    html = []
    self._add_table_row(context, html, row, self._get_cell_viewers(context), row_tag='tr', cell_tag='td')
    return ''.join(html)
       
       
  def as_bootstrap_grid(self, context=None):
    '''Prints the table as a set of row divs with child column divs.  These can be styled to look like a table using CSS.
       If a cell_viewer was specified in a header, the call should include the calling context. 
       Most table functions, like filtering, work with divs.  Sorting by column doesn't work.
       
       For example, to print as a set of bootstrap rows and columns, define the class as:
         class MyTable(ClientSideTable):
           row_css_class = 'row'  # the bootstrap row class
           headings = [
             TableHeader('ID', 'col-md-10'),
             TableHeader('Name', 'col-md-10'),
             TableHeader('Age', 'col-md-4'),
           ]
       Then call table.as_bootstrap_grid() to print as a bootstrap row/column grid.
    '''
    html = []
    
    # set up the cell viewers, if there are any
    cell_viewers = self._get_cell_viewers(context)

    # scripts for behavior
    if self.pagination_links_top:
      self._add_pagination_html(html, True)

    # table header
    html.append('''<div id="%s" class="%s" %s>''' % (self.guid, self.css_class, ' '.join(['%s="%s"' % (k, v) for k, v in list(self.table_attrs.items()) ])))
    if self.show_headings and self.title:
      html.append('''<div class="title">%s</div>''' % (self.title))
      html.append('''</div>''')
                  
    # display the actual table
    if self.show_headings:
      html.append('''<div class="customtable_header_row %s">''' % self.row_css_class)
      for i, heading in enumerate(self.headings):
        if isinstance(heading, TableHeader):
          html.append('''  <div class="customtable_header %s">%s</div>''' % (heading.css_class, heading.title))
        else:
          html.append('''  <div class="customtable_header">%s</div>''' % (heading))
      html.append('''</div>''')

    # print the table
    for row in self:
      self._add_table_row(context, html, row, cell_viewers, row_tag='div', cell_tag='div')
    
    # scripts for behavior
    self._add_extra_html(html)
    self._add_filter_html(html)
    if self.pagination_links_bottom:
      self._add_pagination_html(html, False)
    
    # table footer
    html.append('</div>')
    
    # return the html
    return ''.join(html)       

  
  def as_bootstrap_grid_row(self, row, context=None):
    '''Gets a single table row.  This method is provided for times when only a single row needs to be printed, such
       as an ajax replace of a table row'''
    html = []
    self._add_table_row(context, html, row, self._get_cell_viewers(context), row_tag='div', cell_tag='div')
    return ''.join(html)
    


  def _get_cell_viewers(self, context):
    '''Creates the cell viewer objects'''
    cell_viewers = {}
    for i, heading in enumerate(self.headings):
      if isinstance(heading, TableHeader) and heading.cell_viewer:
        assert context != None, 'Tables with cell viewers must be called with table.get_html(context).'
        cell_viewers[i] = getattr(context['self'], heading.cell_viewer)
    return cell_viewers


  def _add_table_row(self, context, html, row, cell_viewers, row_tag, cell_tag, col_start=0, col_end=0):
    '''Adds a row of the table.'''
    if isinstance(row, TableRow):  # specialized list
      html.append('''<%s class="%s %s">''' % (row_tag, self.row_css_class, row.css_class))
    else: # regular list
      html.append('''<%s class="%s">''' % (row_tag, self.row_css_class))
    for colnum in range(col_start, len(self.headings) if col_end == 0 else col_end):
      val = row[colnum] if colnum < len(row) else None
      attrs = {
        'class': [ 'customtable_cell' ],
      }
      # add formatting from the table cell
      if isinstance(val, TableCell):
        if val.attrs:
          attrs.update(val.attrs)
        attrs['class'].append(val.css_class)
        val = val.value
      # add formatting from the heading for this column
      if isinstance(self.headings[colnum], TableHeader):
        attrs['class'].append(self.headings[colnum].css_class)
        # do we have a string formatter like "%.2f"
        if self.headings[colnum].formatter:   
          val = self.headings[colnum].formatter % val if val != None else val
        # do we need lazy evaluation of the cell value using a Mako Def
        if self.headings[colnum].cell_viewer: 
          assert isinstance(val, (tuple, list)), 'Tables with cell viewers must be have list/tuple values specifying the positional function arguments (column %s value has type %s instead of a list/tuple).' % (colnum, type(val))
          val = mako.runtime.capture(cell_viewers[colnum].args[0], cell_viewers[colnum], *val)
      # output the cell
      html.append('''  <%s %s>%s</%s>''' % (cell_tag, flat_attr(attrs), val, cell_tag))
    html.append('''  </%s>''' % (row_tag))
        
    
  def _add_extra_html(self, html):
    '''Subclasses can add things here'''
    pass
    
    
  def _add_sorter_html(self, html):
    # short circuit if the table doesn't sort
    if not self.sortable:
      return ''
    # initial options
    options = {}
    # determine if any columns are not sortable
    options['headers'] = {}
    for i, heading in enumerate(self.headings):
      if isinstance(heading, TableHeader) and not heading.sortable:
        options['headers'][i] = { 'sorter': False }
    # return the script
    html.append(scriptify('''
      $(function() {
        $('#table_%(guid)s')
          .tablesorter(%(options)s)
          .off('sortEnd.%(guid)s')
          .on('sortEnd.%(guid)s', function() {
            // reload the existing page since the rows on this page probably changed
            $('#%(guid)s').find('ul.pagination').find('a.pagination_link_active').trigger('click.%(guid)s');
          })//on
        ;//table
      });//ready
    ''' % {
      'guid': self.guid,
      'options': json.dumps(options),
    }))
    
    
  def _add_filter_html(self, html):
    html.append(scriptify('''
      $(function() {
        var table_div = $('#%(guid)s');
        var controls = $('%(filter_controls_selector)s');
        
        // runs the filter
        table_div.off('customtable_run_filter').on('customtable_run_filter', function() {
          // enable/disable the filter on each table row
          table_div.children('table').children('tbody').children('.customtable_row').each(function() { // there MUST be a better way to do this, but I want to select only the immediate table, not any embedded tables
            // trigger the filters for this row
            var cfe = $.Event('customtable_filter', { filtered: false, row: this });
            table_div.triggerHandler(cfe);
            
            // filter based on the event value
            $(this).toggleClass('customtable_filtered', cfe.filtered);
          });//table_div
          
          // trigger the pagination to refresh
          table_div.trigger('customtable_paginate');
        });//filter event
        
        // CONTAINS text matching controls
        controls.find('[data-filter-type="contains-match"]').each(function() {
          // initial setup
          var target_selector = $(this).attr('data-filter-target-selector');
          var match_value = $(this).val();
          // refilter the table when changed
          $(this).on('change', function() {
            match_value = $(this).val().toUpperCase();
            table_div.trigger('customtable_run_filter');
          });//change
          // callback that filters records based on the current value
          table_div.on('customtable_filter', function(event) {
            if (!event.filtered && match_value != '') {
              event.filtered = $(event.row).find(target_selector).text().toUpperCase().indexOf(match_value) < 0;
            }//if
          });//customtable_filter        
        });//each
        
        // EXACT text matching controls
        controls.find('[data-filter-type="exact-match"]').each(function() {
          // initial setup
          var target_selector = $(this).attr('data-filter-target-selector');
          var match_value = $(this).val();
          // refilter the table when changed
          $(this).on('change', function() {
            match_value = $(this).val();
            table_div.trigger('customtable_run_filter');
          });//change
          // callback that filters records based on the current value
          table_div.on('customtable_filter', function(event) {
            if (!event.filtered) {
              event.filtered = $(event.row).find(target_selector).text() != match_value;
            }//if
          });//customtable_filter        
        });//each
        
        // REGEX text matching controls (set text field to a regular expression like ^match$ for an exact match)
        controls.find('[data-filter-type="regex-match"]').each(function() {
          // initial setup
          var target_selector = $(this).attr('data-filter-target-selector');
          var match_re = new RegExp($(this).val());
          // refilter the table when changed
          $(this).on('change', function() {
            match_re = new RegExp($(this).val());
            table_div.trigger('customtable_run_filter');
          });//change
          // callback that filters records based on the current value
          table_div.on('customtable_filter', function(event) {
            if (!event.filtered) {
              event.filtered = !match_re.test($(event.row).find(target_selector).text());
            }//if
          });//customtable_filter        
        });//each        
        
        // RANGE text matching controls (set text field to minval:maxval)
        controls.find('[data-filter-type="range-match"]').each(function() {
          // initial setup
          var target_selector = $(this).attr('data-filter-target-selector');
          var parts = $(this).val().toUpperCase().split(':');
          // refilter the table when changed
          $(this).on('change', function() {
            parts = $(this).val().split(':');
            table_div.trigger('customtable_run_filter');
          });//change
          // callback that filters records based on the current value
          table_div.on('customtable_filter', function(event) {
            if (!event.filtered && parts.length >= 2) {
              var text = $(event.row).find(target_selector).text().toUpperCase();
              event.filtered = (text < parts[0] || text > parts[1]);
            }//if
          });//customtable_filter        
        });//each        
        
      });//ready
    ''' % {
      'guid': self.guid,
      'filter_controls_selector': self.filter_controls_selector,
    }))
    
    
  def _add_pagination_html(self, html, at_top):
    # pagination html/script - pagination can be refreshed if the table is modified client side by JS (filtering, for example)
    if self.rows_per_page == 0 or len(self) <= self.rows_per_page:
      return ''
    html.append('<div class="pagination-container">')
    html.append('<ul class="pagination">')
    html.append('<li class="pagination_item_previous"><a class="pagination_link" data-pageindex="-1">&laquo;</a></li>')
    html.append('<li class="pagination_item_next"><a class="pagination_link" data-pageindex="+1">&raquo;</a></li>')
    html.append('</ul>')
    html.append('</div>')
    if (at_top and not self.pagination_links_bottom) or (not at_top):  # only print once
      html.append(scriptify('''
        $(function() {
          var table_div = $('#%(guid)s');
          var current_pagenum = 0;
          table_div.off('customtable_paginate').on('customtable_paginate', function() {
            var rows_per_page = %(rows_per_page)i;
            var num_pages = 1;  // set below in addPageLinks

            // switches to the given page index
            function switchToPage(pagenum, scroll_to_top) {
              var all_links = table_div.find('ul.pagination > li > a.pagination_link');
              // parse the page number and calculate the rows to show
              if (pagenum == '-1') {
                pagenum = current_pagenum - 1;
              }else if (pagenum == '+1') {
                pagenum = current_pagenum + 1;
              }else{
                pagenum = parseInt(pagenum);
              }//if
              pagenum = Math.max(0, pagenum);
              pagenum = Math.min(num_pages - 1, pagenum);
              var minIndex = pagenum * rows_per_page;
              var maxIndex = minIndex + rows_per_page;
          
              // show the rows
              table_div.children('table').children('tbody').children('.customtable_row').not('.customtable_filtered').each(function(rowIndex) {
                $(this).toggleClass('customtable_hidden', rowIndex < minIndex || rowIndex >= maxIndex);
              });//each
          
              // update the pagination link styles
              all_links.removeClass('pagination_link_active');
              all_links.eq(pagenum+1).addClass('pagination_link_active');
              current_pagenum = pagenum;
            
            }//switchToPage
        
            // adds the links for the pages
            function addPaginationLinks() {
              // remove any existing page links
              var pagination_item_next = table_div.find('.pagination_item_next');
              table_div.find('.pagination_item_direct').remove(); // might be a second run of this method
            
              // add the new page links
              num_pages = Math.ceil(table_div.children('table').children('tbody').children('.customtable_row').not('.customtable_filtered').length / rows_per_page);
              table_div.find(".pagination_pages_total").text(rows_per_page);
              for (var i = 0; i < num_pages; i++) {
                pagination_item_next.before('<li class="pagination_item_direct"><a class="pagination_link" data-pageindex="' + i + '">' + (i+1) + '</a></li>');
              }//for

              // add the page press event to the links
              table_div.find('ul.pagination > li > a.pagination_link').off('click.%(guid)s').on('click.%(guid)s', function() {
                switchToPage($(this).attr('data-pageindex'));
              });//click
            }//addPaginationLinks

            // show only the first page on load
            addPaginationLinks();
            switchToPage(current_pagenum, false);
        
          });//on refresh_pagination
        
          // initial trigger
          table_div.trigger('customtable_paginate');
        });//ready'''
      % {
        'guid': self.guid,
        'rows_per_page': self.rows_per_page,
      }))

    




########################################################################
###   An extension of the client-side table that makes it server-side.
###   Use this type of table when the number or rows is numerous, making
###   a client-side table unmanageable.
###
###   Right now data-filter-type="method-call" is all that is supported.  It calls
###   a method on the table object.
###


class ServerSideTable(ClientSideTable):
  '''Our server-side table.  This is the table we use throughout the site when server-side pagination is needed.'''
  endpoint_url = 'error-you-forgot-to-set-endpoint_url'  # required - the url to call when the table needs to be refreshed (after filtering, sorting, etc.)
  selector = None                                        # the table div selector to replace when table is reloaded from server (defaults to the 'div#guid')

  def __init__(self, request, *args, **kwargs):
    '''Constructor.'''
    super().__init__(request, *args, **kwargs)
    self.num_records = None  # used in pagination below
    self.num_pages = None    # used in pagination below
    # grab the settings from the post
    self.settings = {
      'sort_column': None,
      'sort_ascending': True,
      'current_page': 0,
      'filters': {},
      'rows_per_page': None,
    }
    enc_settings = request.REQUEST.get('server_side_table_settings')
    if enc_settings:
      self.settings.update(json.loads(enc_settings))
    
    
  def as_table(self, context=None):
    '''Returns the html for this table.'''
    assert self.num_records != None and self.num_pages != None, 'Your forgot to call adapt_query before displaying a ServerSideTable.'
    return super().as_table(context)
    
    
  def as_div(self, context=None):
    '''Returns the html for this table.'''
    assert self.num_records != None and self.num_pages != None, 'Your forgot to call adapt_query before displaying a ServerSideTable.'
    return super().as_div(context)
    

  def set_filter_state(self, name, value, filter_type='method-call'):
    ''' 
    Set the state of a filter.
      - Allows python to programmatically configure a filter and then call adapt_query()
    '''
    self.settings['filters'].update({ name: { 'filter_type': filter_type, 'value': value }})


  def adapt_query(self, qry, apply_filtering=True, apply_sorting=True, apply_pagination=True):
    '''Applies the current sort, filters, and pagination to the given query.  This method is typically
       called from the view just before the for-loop going through the query.
    '''
    # apply filtering
    if apply_filtering:
      for filter_id, fltr in list(self.settings['filters'].items()):
        if fltr.get('filter_type') == 'method-call':  # calls filter_id() where id is the id of the html filter element
          qry = getattr(self, 'filter_%s' % filter_id)(qry, fltr.get('value'))
    
    # apply sorting
    if apply_sorting:
      if self.settings['sort_column'] != None and self.settings['sort_column'] < len(self.headings):
        header = self.headings[self.settings['sort_column']]
        if isinstance(header, TableHeader) and header.query_order_by_name:
          if header.query_order_by_case_insensitive:
            qry = qry.extra( select={'lower_%s' % header.query_order_by_name: 'lower(%s)' % header.query_order_by_name}).order_by("%slower_%s" % (not self.settings['sort_ascending'] and '-' or '', header.query_order_by_name))
          else:
            qry = qry.order_by("%s%s" % (not self.settings['sort_ascending'] and '-' or '', header.query_order_by_name))
      
    # apply pagination
    self.num_pages = 0
    if apply_pagination:
      self.num_records = qry.count()
      rows_per_page = self.rows_per_page
      if self.settings['rows_per_page']:
        try:
          rows_per_page = int(self.settings['rows_per_page'])
        except ValueError:
          pass
      if self.num_records != None and rows_per_page > 0 and self.num_records > rows_per_page:
        self.num_pages = math.ceil(float(self.num_records) / float(rows_per_page))
      self.settings['current_page'] = min(self.settings['current_page'] or 0, self.num_pages-1)
      self.settings['current_page'] = max(self.settings['current_page'], 0)
      if self.num_pages > 0:
        qry = qry[self.settings['current_page'] * rows_per_page: (self.settings['current_page']+1) * rows_per_page]
      
    # return the query
    return qry
    
    
    
  def _add_extra_html(self, html):
    html.append(scriptify('''
      $(function() {
        var table_div = $('#%(guid)s');
        
        // the initial settings of the table
        table_div.data('server_side_table_settings', %(settings)s);
        
        // reloads the table via ajax (call when settings change)
        table_div.off('server_side_table_refresh').on('server_side_table_refresh', function() {
          // ensure we aren't calling twice
          if (table_div.data('server_side_table_refreshing')) {
            return;
          }//if
          table_div.data('server_side_table_refreshing', true);  // just in case the event is called twice by bad calling javascript
          
          // run the ajax
          $('%(selector)s').loadReplace('%(endpoint_url)s', {
             'server_side_table_settings': JSON.stringify(table_div.data('server_side_table_settings')),
          });//loadReplace

        });//on
      });//ready
    ''' % {
      'guid': self.guid,
      'settings': json.dumps(self.settings),
      'endpoint_url': self.endpoint_url,
      'selector': self.selector or ('#%s' % self.guid)
    }))
    
  
  def _add_sorter_html(self, html):
    if self.sortable:
      html.append(scriptify('''
        $(function() {
          var table_div = $('#%(guid)s');
          var table = $('#table_%(guid)s');
          
          // add the initial ui for the current sort
          var settings = table_div.data('server_side_table_settings');
          if (settings.sort_column != null) {
            var header = table.find('th.tablesorter').eq(settings.sort_column);
            header.addClass(settings.sort_ascending ? 'tablesorter-headerAsc' : 'tablesorter-headerDesc');
          }//if
          
          // sort event when a header is clicked
          table.find('th.tablesorter').off('click.%(guid)s').on('click.%(guid)s', function() {
            settings = table_div.data('server_side_table_settings');
            var col_index = $(this).parent().children('th.tablesorter').index(this);
            if (settings.sort_column != null && col_index == settings.sort_column) {
              settings.sort_ascending = !settings.sort_ascending;
            }else{
              settings.sort_column = col_index;
              settings.sort_ascending = true;
            }//if
            table_div.data('server_side_table_settings', settings);
            table_div.trigger('server_side_table_refresh');
          });//on
        });//ready
      ''' % {
        'guid': self.guid,
      }))
  
  
  def _add_pagination_html(self, html, at_top):
    if not self.num_pages:
      return ''
    # we need pagination
    html.append('<div class="pagination-container">')
    html.append('<ul class="pagination">')
    html.append('<li class="pagination_item_previous"><a class="pagination_link" data-pageindex="-1">&laquo;</a></li>')
    for i in range(int(self.num_pages)): 
      html.append('<li class="pagination_item_direct"><a class="pagination_link %s" data-pageindex="%i">%i</a></li>' % (i == self.settings['current_page'] and 'pagination_link_active' or '', i, i+1))
    html.append('<li class="pagination_item_next"><a class="pagination_link" data-pageindex="+1">&raquo;</a></li>')
    html.append('</ul>')
    html.append('</div>')
    if (at_top and not self.pagination_links_bottom) or (not at_top):  # only print once
      html.append(scriptify('''
        $(function() {
          var table_div = $('#%(guid)s');
          // page links
          table_div.find('a.pagination_link').off('click.pagination_link').on('click.pagination_link', function() {
            var settings = table_div.data('server_side_table_settings');
            var pageindex = $(this).attr('data-pageindex');
            if (pageindex == "-1") {
              settings.current_page = settings.current_page - 1;
            }else if (pageindex == "+1") {
              settings.current_page = settings.current_page + 1;
            }else{ // direct page number
              settings.current_page = parseInt(pageindex);
            }//if
            table_div.data('server_side_table_settings', settings);
            table_div.trigger('server_side_table_refresh');
          });//click
        
        });//ready'''
      % {
        'guid': self.guid,
        'rows_per_page': self.settings['rows_per_page'] or self.rows_per_page,
      }))

    
    
  def _add_filter_html(self, html):
    html.append(scriptify('''
      $(function() {
        var table_div = $('#%(guid)s');
        var controls = $('%(filter_controls_selector)s');
        
        // change the settings object when a control is changed
        controls.find('[data-filter-type]').each(function() {
          $(this).off('change.serverside-table-filter').on('change.serverside-table-filter', function() {
            var settings = table_div.data('server_side_table_settings');
            settings.filters[$(this).attr('id')] = {
              filter_type: $(this).attr('data-filter-type'),
              value: $(this).val(),
            };
            table_div.data('server_side_table_settings', settings);
          });//change
        });//each
        
      });//ready
    ''' % {
      'guid': self.guid,
      'filter_controls_selector': self.filter_controls_selector,
    }))



