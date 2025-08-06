from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100, blank=True, null=True)
    published_date = models.DateField(blank=True, null=True)
    available_copies = models.PositiveIntegerField(default=0)

    def __str__(self):
        return (f'{self.title} by {self.author} - '
                f'{self.available_copies} copies available')
