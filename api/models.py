from django.db import models
from django.db.models import UniqueConstraint


class Establishment(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    url = models.CharField(max_length=2555, null=True, blank=True)

    def __str__(self):
        return self.name


class Consultant(models.Model):
    name = models.CharField(max_length=255)
    number = models.IntegerField()
    establishment = models.ForeignKey(Establishment, on_delete=models.CASCADE)
    type = models.CharField(max_length=55, choices=[
        ('live', 'LIVE'),
        ('data', 'DATE')
    ])

    class Meta:
        constraints = [
            UniqueConstraint(fields=['establishment', 'number'], name='unique_establishment_number')
        ]

    def __str__(self):
        return self.name


class Client(models.Model):
    email = models.CharField(max_length=255)
    iin = models.CharField(max_length=12)
    status = models.CharField(max_length=50, choices=
    [
        ('waiting', 'WAITING'),
        ('processing', 'PROCESSING'),
        ('finished', 'FINISHED')
    ])
    consultant = models.ForeignKey(Consultant, on_delete=models.CASCADE)

    def __str__(self):
        return self.email


class TimeSlots(models.Model):
    slot = models.CharField(max_length=25)


class Booking(models.Model):
    date = models.DateField(auto_now=True)
    slot = models.ForeignKey(TimeSlots, null=True, blank=True, on_delete=models.SET_NULL)
    consultant = models.ForeignKey(Consultant, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.consultant.name} - {self.date}"

