import os
try:
    from PIL import Image
except:
    import Image
from cStringIO import StringIO
from uuid import uuid4

from django.core.files.base import ContentFile
from django.template import Library

from thumbnail.models import Thumbnail

register = Library()

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
    
    #do we have a thumbnail by this name?
    thumbnails = Thumbnail.objects.filter(name=miniature)
    if thumbnails:
        thumb = thumbnails[0]
        
    else:
        #create it
        
        #fetch the data (from rackspace, or wherever it might be)
        try:
            data = StringIO(file.read())
            image = Image.open(data)
        except:
            return None

        #Do the work
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
        
        # now, save it
        
        #prep work
        thumb = Thumbnail(
            name = miniature,
        )
        new_image = StringIO()
        try:
            image.save(new_image, image.format, quality=90, optimize=1)
        except:
            image.save(new_image, image.format, quality=90)
        #put the image data in a django friendly object (https://docs.djangoproject.com/en/dev/ref/files/file/#django.core.files.File)
        myfile = ContentFile(new_image.getvalue())
        
        #save the thumb (https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.fields.files.FieldFile.save)
        thumb.image.save(uuid4().hex + format, myfile)
        
    return thumb.image.url

register.filter(thumbnail)

def square_thumbnail(file, size='104'):
    return thumbnail(file, "%sx%s" % (size, size), square=True)

register.filter(square_thumbnail)