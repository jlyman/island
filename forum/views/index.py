from django.conf import settings
from django.db.models import Count, Min, Max
from django_mako_plus.controller import view_function
from django.http import HttpResponse, HttpResponseRedirect, Http404
from management import models as mmod
from lib.filters import *
from forum import models as fmod
from . import templater, prepare_params
from lib.tables import TableHeader, ServerSideTable


COMMENTS_PER_PAGE = 20


@view_function
def process_request(request):
  # check user permissions and prepare the params
  params = prepare_params(request)
  
  # render the template
  params['table_html'] = get_table(request, as_response=False)
  return templater.render_to_response(request, 'index.html', params)
  
  

@view_function
def get_table(request, as_response=True):
  # check user permissions and prepare the params
  params = prepare_params(request)
  
  # query the threads and prepare the table
  table = ThreadTable(request)
  threads_query = fmod.Thread.objects.order_by('-created')
  threads_query = table.adapt_query(threads_query, apply_filtering=True, apply_sorting=False, apply_pagination=True) # sorting not supported
  counts = dict(((r['thread'], (r['count'], r['latest'])) for r in fmod.Comment.objects.filter(thread__in=threads_query).values('thread').annotate(count=Count('thread'), latest=Max('created'))))

  for thread in threads_query:
    table.append((
      '<div class="icon icon_arrow_right2 icon_1p5x icon_color_gray" aria-label="Arrow Right"></div>',
      thread.created.strftime('%b %d at %H:%M'),
      (thread, ),
      (thread, ),
      (thread, counts.get(thread.id)),
    ))
  
  # return the table
  params['table'] = table
  if as_response:
    return templater.render_to_response(request, 'index.get_table.html', params)
  return templater.render(request, 'index.get_table.html', params)
  
  
  
class ThreadTable(ServerSideTable):
  '''Our table of threads to display'''
  headings = [ 
    TableHeader('', 'col_icon'),
    TableHeader('Posted', 'col_date'), 
    TableHeader('Title', 'col_title', cell_viewer='title_viewer'), 
    TableHeader('Topic', 'col_topic', cell_viewer="topic_viewer"), 
    TableHeader('', 'col_comments', cell_viewer='comments_viewer'), 
  ]
  css_class = 'customtable table table-hover'
  sortable = False
  rows_per_page = COMMENTS_PER_PAGE
  endpoint_url = '/forum/index.get_table'
  
