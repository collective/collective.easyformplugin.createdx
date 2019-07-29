.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

==================================
collective.easyformplugin.createdx
==================================

Create dexterity objects from easyform submissions

Features
--------

- Easyform action to create dexterity items
- Converters to meet the target fields requirements for example a data_handler to add timezone info to be able to create events.


Documentation
-------------

- Install the addon within your Plone site
- From the actions menu choose edit actions and add a new action "Create dexterity content"
- Choose a location where the items should be create
- Choose the desired content_type
- Map your form field ids to the item field ids and add the converter configuration if needed

Mapping example
---------------
```
topic title
comments text:richtext
event_start start:datetime
```


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
