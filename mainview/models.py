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


class Rent(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    rent_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(blank=True, null=True)
    returned = models.BooleanField(default=False)
    returned_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} rented {self.book.title} on {self.rent_date.strftime("%Y-%m-%d %H:%M:%S")}'