import django.forms 
import django.forms.widgets
from django.utils.encoding import force_text
from django.utils.html import conditional_escape, format_html
from django.utils.safestring import mark_safe
from django.forms.util import flatatt
import itertools


#################################################
###   Icon Button Widget

class ButtonChoiceWidget(django.forms.Select):
  '''A radio choice that displays as a Bootstrap set of buttons.'''
  def __init__(self, btn_class="btn btn-default", div_attrs={}, *args, **kwargs):
      self.btn_class = btn_class
      self.div_attrs = div_attrs
      super().__init__(*args, **kwargs)

  def render(self, name, value, attrs=None, choices=()):
    if value is None: value = ''
    if attrs == None:
      attrs = {}
    attrs['data-toggle'] = 'buttons'
    attrs.update(self.div_attrs)
    final_attrs = self.build_attrs(attrs)
    output = []
    output.append(format_html('<div{0}>', flatatt(final_attrs)))
    options = self.render_options(attrs['id'], name, choices, [value])
    if options:
      output.append(options)
    output.append('</div>')
    return mark_safe('\n'.join(output))
      

  def render_options(self, elem_id, name, choices, selected_choices):
    selected_choices = set(force_text(v) for v in selected_choices)
    output = []
    for i, (option_value, option_label) in enumerate(itertools.chain(self.choices, choices)):
      option_value = force_text(option_value)
      btn_class = mark_safe(self.btn_class)
      checked = ''
      if option_value in selected_choices:
          btn_class = mark_safe('%s %s' % (btn_class, 'active'))
          checked = 'checked'
      output.append(format_html('<label class="{0}"><input type="radio" value="{1}" name="{2}" id="{3}" {4} autocomplete="off"/>{5}</label>',
                         btn_class,
                         option_value,
                         name,
                         '%s_%s' % (elem_id, i),
                         checked,
                         option_label))
    return '\n'.join(output)

