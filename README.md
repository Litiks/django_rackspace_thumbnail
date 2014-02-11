django_rackspace_thumbnail
==========================

A simple django app to generate thumbnails for image files stored via django_cumulus

This app was created because easy_thumbnails lacked support for django 1.2

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


