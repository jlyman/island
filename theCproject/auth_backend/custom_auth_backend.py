# import the User object
from django.contrib.auth.models import User
from management import models as mmod
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
      search_tree = c.search('uid=' + ry_username +', ou=people, o=byu.edu','(objectClass=*)', SEARCH_SCOPE_WHOLE_SUBTREE, attributes=['cn', 'permanentPhone', 'mail', 'employeeType'])
      attributes = c.response[0].get('attributes')
    except LDAPException:
      return None

    # next, ensure the user exists
    try:
      # Try to find a user matching your username
      user = mmod.SiteUser.objects.get(username=ry_username)

    except mmod.SiteUser.DoesNotExist:
      user = mmod.SiteUser()
      user.username = ry_username

    # finally, update the user information from ldap
    import pprint; pprint.pprint(attributes)

    user.fullname = attributes.get('cn')[0] if attributes.get('cn') else ''
    user.email = attributes.get('mail')[0] if attributes.get('mail') else ''
    user.phone = attributes.get('permanentPhone')[0] if attributes.get('permanentPhone') else ''
    user.BYU_status = ','.join(attributes.get('employeeType')) if attributes.get('employeeType') else ''
    user.save()  

    # return the user
    return user


  # Required for your backend to work properly - unchanged in most scenarios
  def get_user(self, user_id):
    try:
      return mmod.SiteUser.objects.get(pk=user_id)
    except:
      return None