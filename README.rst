ChunkyCMS
---------------

.. image:: https://secure.travis-ci.org/Trion/chunkycms.png?branch=master

A simple Content Management System for Django.

It's more a project to learn best practise in programming and tool usage.

Requirements
============

* Django >= 1.5
* South >= 0.7.6 (optional) 


Installation
============

Currently you cannot install it with pip. You need to fetch the repository and run::

    $ git clone git://github.com/Trion/chunkycms.git
    $ python setup.py install

You need modify the following files.

settings.py::

    INSTALLED_APPS = (
        ...
        "chunkycms",
        ...
    )

    ...

    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        "chunkycms.context_processors.live_edit",
        ...
    )

urls.py (catches all requests, that doesn't match anywhere else)::

    urlpatterns = patterns('',
        ...
        url(r'^', include('chunkycms.urls'), name='chunkycms')
    )

Usage
=====

TBD
