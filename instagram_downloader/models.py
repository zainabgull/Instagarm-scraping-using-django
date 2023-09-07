# models.py
from django.db import models

class ScrapedInstagramImage(models.Model):
    hashtag = models.CharField(max_length=100)
    image_url = models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.hashtag
