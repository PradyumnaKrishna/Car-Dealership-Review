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


class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return f"Dealer name: {self.full_name}"


class DealerReview:
    def __init__(self, name, dealership, review, purchase, id, purchase_date=None, car_make=None, car_model=None,
                 car_year=None, sentiment=None):
        self.name = name
        self.dealership = dealership
        self.review = review
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id

    def __str__(self):
        return f"Review: {self.review}"
