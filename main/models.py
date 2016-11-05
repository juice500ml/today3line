from django.db import models
from django.utils import timezone

class ParsedData(models.Model):
    url = models.TextField(primary_key=True,)
    title = models.TextField()
    image_url = models.TextField()
    line1 = models.TextField()
    line2 = models.TextField()
    line3 = models.TextField()
    dirty = models.BooleanField()

    def publish(self, title, url, image_url, line1, line2, line3, dirty):
        self.title = title
        self.url = url
        self.image_url = image_url
        self.line1 = line1
        self.line2 = line2
        self.line3 = line3
        self.dirty = dirty

    def __str__(self):
        return str(self.url) + '(' + str(self.dirty) + ')'
