django_rackspace_thumbnail
==========================

A simple django app to generate thumbnails for image files stored via django_cumulus

This app was created because easy_thumbnails lacked support for django 1.2, but it works well for all versions of django.
It alsp supports temp_urls, and it's very quick. We make use of django's default cache if available, and we only perform remote api calls when the thumbnail gets generated.


Installation
------------

- using pip: `pip install https://github.com/Litiks/django_rackspace_thumbnail/archive/master.zip`
- or: add to your requirements.txt: `-e git+https://github.com/Litiks/django_rackspace_thumbnail.git#egg=django_rackspace_thumbnail`
- or: copy the 'thumbnail' folder to your python working directory


Setup
-----

1.Add to Installed Apps::

    INSTALLED_APPS += (
        'thumbnail',
    )
    
2.Sync/Migrate::

    python manage.py syncdb
    # or
    python manage.py migrate thumbnail

    
Usage
-----

In templates::

    {% load thumbnail_tags %}
    <img src='{{ profile.image|thumbnail:"100x100" }}'>


