==================================
collective.easyformplugin.createdx
==================================

Create dexterity objects from easyform submissions

Features
--------

`Easyform <https://pypi.org/project/collective.easyform/>`_ action to create dexterity items.

Converters to meet the target fields requirements for example a data_handler to add timezone info to be able to create events.


Documentation
-------------

- Install the addon within your Plone site
- From the actions menu choose edit actions and add a new action
  ``Create dexterity content``
- Choose a location where the items should be create
- Choose the desired content type
- Map your form field ids to the item field ids and add converters as needed


Available converters
--------------------

``plaintext_to_intellitext``
  converts plain text to html

``datetime_with_timezone``
  adds portal default timezone to datetime

``file_converter``
  takes a fileupload and converts it to a named blob file,



Mapping
-------

Field mapping format: ``formFieldId itemFieldId:converter``.
The ``converter`` is optional, value is taken as is.
Latter implies fields are matching in easyform and target schema!
Make sure you have at least eiter the ``title`` or ``id`` mapping defined, because it will also be used to create the id of the item!

Example::

    topic title
    comments text:plaintext_to_intellitext
    event_start start:datetime_with_timezone
    video_upload file:fileupload_converter


Note
----

There have been ZODB transaction issues, turn off versioning for easyform as a workaround.

Contribute
----------

- Issue Tracker: https://github.com/collective/collective.easyformplugin.createdx/issues
- Source Code: https://github.com/collective/collective.easyformplugin.createdx
- Documentation: https://docs.plone.org/foo/bar


Support
-------

If you are having issues, please let us know on the issue tracker.


License
-------

The project is licensed under the GPLv2.
