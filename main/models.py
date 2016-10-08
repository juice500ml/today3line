from django.db import models
from django.utils import timezone

class Update(models.Model):
    user_hash = models.TextField()
    index = models.IntegerField()
    title = models.TextField()
    url = models.TextField()
    image_url = models.TextField()
    line1 = models.TextField()
    line2 = models.TextField()
    line3 = models.TextField()

    def publish(self, user_hash, index, title, url,
            image_url, line1, line2, line3):
        self.user_hash = user_hash
        self.index = index
        self.title = title
        self.url = url
        self.image_url = image_url
        self.line1 = line1
        self.line2 = line2
        self.line3 = line3

    def __str__(self):
        return str(self.title) + '(' + str(self.user_hash) + ')'
