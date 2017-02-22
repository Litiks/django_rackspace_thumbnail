import hashlib
from django.db import models

class Thumbnail(models.Model):
    hexdigest = models.CharField(max_length=32, db_index=True)
    name = models.TextField()   # basically only used to generate the md5
    image = models.ImageField(upload_to='thumbnails')

    def save(self, *args, **kwargs):
        if not self.hexdigest:
            self.hexdigest = hashlib.md5(self.name).hexdigest()
        super(Thumbnail, self).save(*args, **kwargs)
