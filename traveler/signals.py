import urllib2

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from social_auth.signals import socialauth_registered

from traveler import models

def new_users_handler(sender, user, response, details, **kwargs):
    '''
    This signal fires when a new social_auth user is created and populates
    fields in the locast user profile with data retrieved from Facebook.
    '''
    social_auth_user = user.social_auth.all()[0]

    user_profile = models.LocastUserProfile()
    user_profile.bio = social_auth_user.extra_data.get('bio', '')
    user_profile.user = user
    try:
        url = "http://graph.facebook.com/%s/picture?type=large" % ( 
                social_auth_user.extra_data['id'] )
        ext = 'jpg'
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(urllib2.urlopen(url).read())
        img_temp.flush()
        img_temp.seek(0)

        user_profile.user_image.save(
            '%s.%s' %( social_auth_user.extra_data['id'], ext),
            File(img_temp)
        )
    except:
        pass

    user_profile.save()

    return False

socialauth_registered.connect(new_users_handler, sender=None)
