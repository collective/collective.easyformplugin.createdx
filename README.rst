==================================
collective.easyformplugin.createdx
==================================

Create dexterity objects from easyform submissions

Features
--------

- Easyform action to create dexterity items
- Converters to meet the target fields requirements for example a data_handler
  to add timezone info to be able to create events.


Documentation
-------------

- Install the addon within your Plone site
- From the actions menu choose edit actions and add a new action
  "Create dexterity content"
- Choose a location where the items should be create
- Choose the desired content type
- Map your form field ids to the item field ids and add converters as needed


Available converters
--------------------

- 'plaintext_to_intellitext': converts plain text to html,
- 'datetime_with_timezone': adds portal default timezone to datetime,



Mapping 
-------

Example::

    topic title
    comments text:richtext
    event_start start:datetime


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
