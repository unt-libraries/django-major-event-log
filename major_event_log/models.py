import uuid
from django.db import models

class Event(models.Model):
    OUTCOME_CHOICES = (
        ("http://purl.org/NET/UNTL/vocabularies/eventOutcomes/#success", "Success"),
        ("http://purl.org/NET/UNTL/vocabularies/eventOutcomes/#failure", "Failure"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # new for django 1.8
    title = models.CharField(max_length=100)
    detail = models.TextField()
    outcome = models.CharField(max_length='80',
                               choices=OUTCOME_CHOICES)
    outcome_detail = models.TextField()
    date = models.DateTimeField()
    entry_created = models.DateTimeField(auto_now_add=True)
    entry_modified = models.DateTimeField(auto_now=True)
    contact_name = models.CharField(max_length=100, help_text="Name that will appear as the Reporting Agent associated with this Major Event")
    contact_email = models.EmailField()

    class Meta:
        ordering = ["date"]

    def __unicode__(self):
        return self.title
