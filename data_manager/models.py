
# Create your models here.
from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField

from data_manager.constants import FEATURE_TYPES, FEATURE_TYPE_CHOICES, FREQUENCY_UNIT_CHOICES, FREQUENCY_UNIT_TYPES, \
    FREQUENCY_USAGE_PREFERENCES, FREQUENCY_USAGE_PREFERENCE_CHOICES
from helpers.models import BaseModel


class FileFeatureSettings(BaseModel):
    feature_name = models.CharField(max_length=255)
    feature_type = models.PositiveSmallIntegerField(choices=FEATURE_TYPE_CHOICES,
                                                    default=FEATURE_TYPES['EXPORT'])
    column_data = JSONField(default=dict)
    columns = ArrayField(models.CharField(max_length=100), null=True, blank=True)
    frequency = models.IntegerField(default=1)
    frequency_unit = models.PositiveSmallIntegerField(choices=FREQUENCY_UNIT_CHOICES,
                                                      default=FREQUENCY_UNIT_TYPES['DAILY'])
    generation_time = models.TimeField(null=True, blank=True)
    usage_preference = models.PositiveSmallIntegerField(choices=FREQUENCY_USAGE_PREFERENCE_CHOICES,
                                                        default=FREQUENCY_USAGE_PREFERENCES['FREQUENCY'])

    def __str__(self):
        return self.feature_name

    @property
    def _feature_type(self):
        return FEATURE_TYPE_CHOICES[self.feature_type-1][1]
