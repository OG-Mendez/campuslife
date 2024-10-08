from django.db import models

# Create your models here.


class Picture(models.Model):
    lodge_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='pictures/')
    lodge_location = models.CharField(max_length=100)
    lodge_price = models.IntegerField(null=True, blank=True)
    available_vacancy = models.IntegerField(default=0)
    caretaker_number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.lodge_name
