from django.db import models

class Thumbnail(models.Model):
    name = models.TextField(db_index=True)
    image = models.ImageField(upload_to='thumbnails')
    
#eof
