import os
import hashlib
try:
    from PIL import Image
except:
    import Image
from cStringIO import StringIO
from uuid import uuid4

from django.core.files.base import ContentFile
from django.core.cache import cache
from django.template import Library

# this is a little dirty.. but it works for me.
try:
    from cumulus.settings import CUMULUS
    IMAGE_URL_TIMEOUT = CUMULUS.get('X_TEMP_URL_TIMEOUT', 86400)
except:
    IMAGE_URL_TIMEOUT = 86400

from thumbnail.models import Thumbnail

register = Library()
cache_prefix = "thumbnails-eep4zejdoc0bi"   # This is just a random string

def thumbnail(file, size='104x104', square=False):
    """
    Returns a thumbnail image of the specified file. (Rendering one if necessary)
    """
    if not file:
        return None
        
    # defining the size
    x, y = [int(x) for x in size.split('x')]
    # defining the filename and the miniature filename
    basename, format = os.path.splitext(file.name)
    if square:
        miniature = basename + '_' + size + '_sq' + format
    else:
        miniature = basename + '_' + size + format
    
    cache_key = cache_prefix + miniature
    # Memcached doesn't like spaces?
    cache_key = cache_key.replace(' ', '_')

    # we can cache the url that we return, but not forever. 
    # specifically, If we're using a 3rd party file server (ie:cumulus), we might be generating a 'temporary url', which often has a short timeout.
    url_cache_key = cache_key + "url"
    url = cache.get(url_cache_key)
    if url:
        return url

    #do we have a thumbnail by this name?
    thumb = cache.get(cache_key)
    if not thumb:
        #check the database
        hexdigest = hashlib.md5(miniature).hexdigest()
        thumbnails = Thumbnail.objects.filter(hexdigest=hexdigest)
        if thumbnails:
            thumb = thumbnails[0]
        
        else:
            # Looks like it doesn't exist. Let create it
            
            # load the image data (from rackspace, or wherever it might be)
            try:
                data = StringIO(file.read())
                image = Image.open(data)
            except:
                return None

            # Do the work
            if square:
                width, height = image.size
                if width > height:
                    delta = width - height
                    left = int(delta/2)
                    upper = 0
                    right = height + left
                    lower = height
                else:
                    delta = height - width
                    left = 0
                    upper = int(delta/2)
                    right = width
                    lower = width + upper

                # carryover the image format manually (not sure why this doesn't work automatically)
                image_format = image.format
                image = image.crop((left, upper, right, lower))
                image.format = image_format

            image.thumbnail([x, y], Image.ANTIALIAS)
            
            # Now, save it
            # prep work
            thumb = Thumbnail(
                hexdigest = hexdigest,
                name = miniature,
            )
            new_image = StringIO()
            try:
                image.save(new_image, image.format, quality=90, optimize=1)
            except:
                image.save(new_image, image.format, quality=90)
            # put the image data in a django friendly object (https://docs.djangoproject.com/en/dev/ref/files/file/#django.core.files.File)
            myfile = ContentFile(new_image.getvalue())
            
            # save the thumb (this also saves the thumbnail record) (https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.fields.files.FieldFile.save)
            thumb.image.save(uuid4().hex + format, myfile)

        # cache it
        cache.set(cache_key, thumb, 86400)

    # load the thumbnail (from rackspace, or wherever it might be)
    try:
        url = thumb.image.url
    except:
        return None
    cache.set(url_cache_key, url, IMAGE_URL_TIMEOUT - 60)
    return url

register.filter(thumbnail)

def square_thumbnail(file, size='104'):
    return thumbnail(file, "%sx%s" % (size, size), square=True)

register.filter(square_thumbnail)