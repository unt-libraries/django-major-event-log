Model
=====

Event
-----

Fields
^^^^^^

``id`` - The primary key for each event. Uses the UUID 4 standard.

``title`` - The short, descriptive title for the event.

``detail`` - The longer, more detailed description of the event.

``outcome`` - The event outcome. Two choices are available here: success or
failure, as defined `here <http://digital2.library.unt.edu/vocabularies/eventOutcomes/>`_.

``outcome_detail`` - A more detailed description of the outcome of the event.

``date`` - The event's date and time of occurrence.

``entry_created`` - The date and time that the event was created in the database.

``entry_modified`` - The date and time that the event was last modified in the
database.

``contact_name`` - The name of the individual or organization who created the
event, or which is responsible for managing the events.

``contact_email`` - The email address for that individual or organization.


Methods
^^^^^^^

``get_absolute_url()`` - This method simply returns the absolute url which
points to the event's own details page, minus the domain.

``is_success()`` - This method returns a boolean (True or False) which
indicates if the chosen value for ``outcome`` was success. So, if the event
outcome was a success, then this method would return ``True``.
