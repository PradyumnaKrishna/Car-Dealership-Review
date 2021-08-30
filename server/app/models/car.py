from django.db import models
from django.utils.timezone import now


class CarMake(models.Model):

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f'Maker: {self.name}'


class CarModel(models.Model):

    SEDAN = 'S'
    SUV = 'U'
    WAGON = 'W'
    MUSCLE = 'M'
    CAR_TYPE_CHOICES = (
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
        (MUSCLE, 'Muscle'),
    )

    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    dealer_id = models.IntegerField(null=True)
    type = models.CharField(max_length=1, choices=CAR_TYPE_CHOICES)
    year = models.DateField(default=now)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Model: {self.name}'
