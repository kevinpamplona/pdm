from django.db import models
from django.core.exceptions import FieldError

# Create your models here.

class StageManager(models.Manager):
    @staticmethod
    def make_stage(w, h, dat, user):
        if w <= 0 or h <= 0 or w*h > Stage.MAX_SIZE:
            raise FieldError("Invalid width or height")

        return Stage(width = w, height = h, data = dat, owner = user)

# When creating new objects, please use Stage.objects.make_stage() instead of the standard Stage().
# This allows the StageManager class above to do extra error checking when creating the stage.
# (The Django documentation does not recommend overwriting __init__ because it can create unexpected 
#   bugs, so it suggested this method instead.)
class Stage(models.Model):
    MAX_SIZE = 65536 # Max size of stage, width * height must be less than or equal to this. Actual number is arbitrary
    width    = models.PositiveSmallIntegerField()
    height   = models.PositiveSmallIntegerField()
    data     = models.CharField(max_length = MAX_SIZE)
    owner    = models.CharField(max_length = 255)
    objects  = StageManager()   # Redirects Stage.objects to be the custom StageManager instead of 
                                #  traditional models.Manager, allowing for make_stage while keeping
                                #  all the regular functionality

class Block(models.Model):
    ID = models.CharField(max_length = 1, primary_key = True)
    sprite = models.URLField()
