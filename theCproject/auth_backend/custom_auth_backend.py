# import the User object
from django.contrib.auth.models import User
from homepage import models as hmod
from ldap3 import Server, Connection, LDAPException, AUTH_SIMPLE, STRATEGY_SYNC, GET_ALL_INFO, SEARCH_SCOPE_WHOLE_SUBTREE

# Name my backend 'MyCustomBackend'
class CustomBackend:

  # Create an authentication method
  # This is called by the standard Django login procedure
  def authenticate(self, ry_username=None, ry_password=None):
    # first check against BYU LDAP
    s = Server('ldap.byu.edu', port = 636, get_info = GET_ALL_INFO, use_ssl = True)
    try: 
      c = Connection(s, auto_bind = True, client_strategy = STRATEGY_SYNC, user="uid=" + ry_username + ", ou=people, o=byu.edu", password=ry_password, authentication=AUTH_SIMPLE)  
    except LDAPException:
      return None
    
    # next, get the user attributes from ldap
    try:
      search_tree = c.search('uid=' + ry_username +', ou=people, o=byu.edu','(objectClass=*)', SEARCH_SCOPE_WHOLE_SUBTREE, attributes=['cn', 'permanentPhone', 'mail', 'employeeType', 'preferredfirstname', 'givenname', 'sn' ])
      attributes = c.response[0].get('attributes')
    except LDAPException:
      return None

    # next, ensure the user exists
    try:
      # Try to find a user matching your username
      user = hmod.SiteUser.objects.get(username=ry_username)

    except hmod.SiteUser.DoesNotExist:
      user = hmod.SiteUser()
      user.username = ry_username

    user.fullname = attributes.get('cn')[0] if attributes.get('cn') else ''
    user.prefname = attributes.get('preferredfirstname')[0] if attributes.get('preferredfirstname') else ''
    user.surname = attributes.get('sn')[0] if attributes.get('sn') else ''
    user.email = attributes.get('mail')[0] if attributes.get('mail') else ''
    user.phone = attributes.get('permanentPhone')[0] if attributes.get('permanentPhone') else ''
    user.byu_status = ','.join(attributes.get('employeeType')) if attributes.get('employeeType') else ''
    user.save()  
    print(user.get_full_name())

    # return the user
    return user


  # Required for your backend to work properly - unchanged in most scenarios
  def get_user(self, user_id):
    try:
      return hmod.SiteUser.objects.get(pk=user_id)
    except:
      return None