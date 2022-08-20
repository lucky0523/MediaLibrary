import logging
from django.db import models

from MediaLibrary.common import Static

LOG_TAG = '[MediaModel.models] '
logging.basicConfig(level=Static.LOG_LEVEL, format='%(asctime)s - %(name)s %(levelname)s - %(message)s')
logger = logging.getLogger(LOG_TAG)


class HardDisk(models.Model):
    vendor = models.CharField(max_length=100, default="", null=True, blank=True)
    series = models.CharField(max_length=100, default="", null=True, blank=True)
    sn = models.CharField(max_length=100, default="", null=True, blank=True)
    capacity = models.IntegerField(default=0)

    def __str__(self):
        return 'Hard disk info:\r\nVendor:{}\r\nSeries:{}\r\nSN:{}\r\nCapacity:{}TB' \
            .format(self.vendor,
                    self.series,
                    self.sn,
                    self.capacity)
