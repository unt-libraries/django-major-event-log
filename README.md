Notice!
------------------------------------------------------------

**This application is still being developed! Major components are still in an
unfinished state!**

Django Major Event Log App
============================================================

About
--------------------------

This django appplication is designed to keep track of major premis events.
The app takes care of both creating and viewing these events. The admin site is
reponsible for managing the actual events, which includes creating them as well
as making modifications to the event date, contact info, description, etc. The
other pages are responsible for displaying events with various levels of
detail.

Each premis event MUST contain the following information:

* Event ID
* Title
* Details
* Outcome
* Outcome Details
* Event Date
* Event Creation Date
* Event Last Modified Date
* Contact Name
* Contact Email

The **Index** page displays all of the created events, in reverse chronological
order (most recent Event Date first). The title, event date, ID, and
outcome are all displayed on this page. The title of each event is
clickable and takes you to the details page for that specific event.

The **Event Details** page displays all the information about a specific event.
On top of displaying all the information in a human-readable form, this page
provides links to the premis xml representation of the event, as well as an
atom item for the event, which contains all the premis xml wrapped in the atom
item.

The **Atom Feed** page, linked to in the navigation bar of each html page,
provides an atom feed for the ten most recent events. Again, these are
sorted by the event date, not the creation or modified dates.

Finally, there is also a small `About` page which contains a description of the
application.

Installation
--------------------------

1.  Download Source

    To get the application, download the source code from the Github repository
    [here](http://example.com).

2.  Install

    Install with `pip install https://github.com/unt-libraries/django-major-event-log`
    
License
-------------------------

See LICENSE

Contributors
-------------------------

Django-major-event-log was developed at the UNT Libraries.

Contributors:

* [Mark Phillips](https://github.com/vphill)
* [Gio Gottardi](https://github.com/somexpert)

