from django_mako_plus.controller.router import MakoTemplateRenderer
from django_mako_plus.controller import RedirectException
from django.dispatch import receiver
from django_cas_ng.signals import cas_user_authenticated
from homepage import models as hmod
from forum import models as fmod

###################################################
###   Create the emplater for this app once
templater = MakoTemplateRenderer('homepage')


###################################################
###   Helper functions used throughout the app

def prepare_params(request, require_authenticated=True):
  '''Creates a parameters dictionary for the current request.'''
  params = {}
  
  # users have to be logged in to be anywhere in this app
  if require_authenticated and not request.user.is_authenticated():
    raise RedirectException('/homepage/login/')

  # get the latest job postings and latest topics
  params['latest_jobs'] = fmod.Thread.objects.filter(topic__title='Jobs').order_by('-created')
  params['latest_threads'] = fmod.Thread.objects.exclude(topic__title='Jobs').order_by('-created')

  # return the parameters
  return params
  
  
  
###########################################################
###   Signal handler for when users authenticate via CAS

@receiver(cas_user_authenticated)
def cas_authentication_handler(sender, **kwargs):
  user = kwargs['user']
  attributes = kwargs['attributes']

  # fill out the user account with info from BYU
  for fieldname, attrname in [
    ( 'first_name', 'preferredFirstName' ),
    ( 'last_name', 'preferredSurname' ),
    ( 'email', 'emailAddress' ),
    ( 'fullname', 'fullName' ),
  ]:
    if attributes.get(attrname):
      setattr(user, fieldname, attributes.get(attrname))
    else:
      setattr(user, fieldname, '')
      
  # byu status logic
  status_list = []
  for attrname in [
    'activeParttimeEmployee',
    'activeFulltimeEmployee',
    'activeFulltimeInstructor',
    'inactiveFulltimeInstructor',
    'activeParttimeNonBYUEmployee',
    'inactiveParttimeNonBYUEmployee',
    'activeEligibletoRegisterStudent',
    'inactiveFulltimeNonBYUEmployee',
    'inactiveParttimeInstructor',
    'inactiveParttimeEmployee',
    'activeFulltimeNonBYUEmployee',
    'inactiveFulltimeEmployee',
    'activeParttimeInstructor',
    'alumni',
  ]:
    if attributes.get(attrname) == 'true':
      status_list.append(attrname)
  user.byu_status = ','.join(status_list)
  
  # save the user
  user.save()
  