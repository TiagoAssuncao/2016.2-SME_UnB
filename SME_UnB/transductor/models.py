from __future__ import unicode_literals

from django.db import models
from django.core.validators import RegexValidator
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator


class TransductorModel(models.Model):
    name = models.CharField(max_length=50, unique=True)
    internet_protocol = models.CharField(max_length=50)
    serial_protocol = models.CharField(max_length=50)
    register_addresses = ArrayField(models.IntegerField())

    def __str__(self):
        return self.name


class Transductor(models.Model):
    model = models.ForeignKey(TransductorModel)
    serie_number = models.IntegerField(default=None)
    ip_address = models.CharField(max_length=15, unique=True, validators=[
        RegexValidator(
            regex='^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$',
            message='Incorrect IP address format',
            code='invalid_ip_address'
        ),
    ])
    description = models.TextField(max_length=150)
    creation_date = models.DateTimeField('date published')

    class Meta:
        abstract = True
        permissions = (
            ("can_view_transductors", "Can view Transductors Page"),
        )

class EnergyTransductor(Transductor):

    def __str__(self):
        return self.description


class Measurements(models.Model):

    collection_date = models.DateTimeField('date published')

    class Meta:
        abstract = True


class VoltageMeasurements(Measurements):
    MAX_VOLTAGE = 280.0
    MIN_VOLTAGE = 100.0

    voltage_a = models.FloatField(default=None, validators=[MinValueValidator(MIN_VOLTAGE), MaxValueValidator(MAX_VOLTAGE)])
    voltage_b = models.FloatField(default=None, validators=[MinValueValidator(MIN_VOLTAGE), MaxValueValidator(MAX_VOLTAGE)])
    voltage_c = models.FloatField(default=None, validators=[MinValueValidator(MIN_VOLTAGE), MaxValueValidator(MAX_VOLTAGE)])


class CurrentMeasurements(Measurements):
    MIN_CURRENT = 5.0
    MAX_CURRENT = 15.0

    current_a = models.FloatField(default=None, validators=[MinValueValidator(MIN_CURRENT), MaxValueValidator(MAX_VOLTAGE)])
    current_b = models.FloatField(default=None, validators=[MinValueValidator(MIN_VOLTAGE), MaxValueValidator(MAX_VOLTAGE)])
    current_c = models.FloatField(default=None, validators=[MinValueValidator(MIN_VOLTAGE), MaxValueValidator(MAX_VOLTAGE)])


class ActivePowerMeasurements(Measurements):
    MIN_ACTIVE = 90.0
    MAX_ACTIVE = 130.0

    active_power_a = models.FloatField(default=None, validators=[MinValueValidator(MIN_ACTIVE), MaxValueValidator(MAX_ACTIVE)])
    active_power_b = models.FloatField(default=None, validators=[MinValueValidator(MIN_ACTIVE), MaxValueValidator(MAX_ACTIVE)])
    active_power_c = models.FloatField(default=None. validators=[MinValueValidator(MIN_ACTIVE), MaxValueValidator(MAX_ACTIVE)])


class ReactivePowerMeasurements(Measurements):
    MIN_REACTIVE = 0.5
    MAX_REACTIVE = 2.0

    reactive_power_a = models.FloatField(default=None, validators=[MinValueValidator(MIN_REACTIVE), MaxValueValidator(MAX_REACTIVE)])
    reactive_power_b = models.FloatField(default=None, validators=[MinValueValidator(MIN_REACTIVE), MaxValueValidator(MAX_REACTIVE)])
    reactive_power_c = models.FloatField(default=None, validators=[MinValueValidator(MIN_REACTIVE), MaxValueValidator(MAX_REACTIVE)])


class ApparentPowerMeasurements(Measurements):
    MIN_APARENT = 90.0
    MAX_APPARENT = 120.0

    apparent_power_a = models.FloatField(default=None. validators=[MinValueValidator(0.9), MaxValueValidator(58)])
    apparent_power_b = models.FloatField(default=None, validators=[MinValueValidator(0.9), MaxValueValidator(58)])
    apparent_power_c = models.FloatField(default=None, validators=[MinValueValidator(0.9), MaxValueValidator(58)])


class EnergyMeasurements(Measurements):

    transductor = models.ForeignKey(EnergyTransductor, on_delete = models.CASCADE)

    def __str__(self):
        return '%s' % self.collection_date

    def calculate_total_active_power(self):
        return (ActivePowerMeasurements.active_power_a + ActivePowerMeasurements.active_power_b + ActivePowerMeasurements.active_power_c)

    def calculate_total_reactive_power(self):
        return (ReactivePowerMeasurements.reactive_power_a + ReactivePowerMeasurements.reactive_power_b + ReactivePowerMeasurements.reactive_power_c)

    def calculate_total_apparent_power(self):
        ap_phase_a = ApparentPowerMeasurements.apparent_power_a
        ap_phase_b = ApparentPowerMeasurements.apparent_power_b
        ap_phase_c = ApparentPowerMeasurements.apparent_power_c

        ap_total = (ap_phase_a + ap_phase_b + ap_phase_c)

        return ap_total
