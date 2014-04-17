from django.db import models
from django.core.exceptions import FieldError

# Create your models here.
DEFAULT = """
 
 S   #   E
 #########
 #########
"""

class StageManager(models.Manager):
    @staticmethod
    def make_stage(w, h, dat, user):
        if w <= 0 or h <= 0 or w*h > Stage.MAX_SIZE:
            raise FieldError("Invalid width or height")

        return Stage(width = w, height = h, data = dat, owner = user)

    @staticmethod
    def default_stage():
        return Stage(
            width = 11,
            height = 5,
            data = DEFAULT,
            owner = '' )

# When creating new objects, please use Stage.objects.make_stage() instead of the standard Stage().
# This allows the StageManager class above to do extra error checking when creating the stage.
# (The Django documentation does not recommend overwriting __init__ because it can create unexpected 
#   bugs, so it suggested this method instead.)
class Stage(models.Model):
    """
    Notes about general protocol for now:
    - 'S': Start position. Must have only one.
    - 'E': End position(s).
    - ' ': Open space.
    - '#': Basic block (floor, wall)
    - '\n': Next row in the stage.
    """
    MAX_SIZE = 65536 # Max size of stage, width * height must be less than or equal to this. Actual number is arbitrary
    width    = models.PositiveSmallIntegerField()
    height   = models.PositiveSmallIntegerField()
    data     = models.CharField(max_length = MAX_SIZE)
    owner    = models.CharField(max_length = 255)
    rating   = 0
    objects  = StageManager()   # Redirects Stage.objects to be the custom StageManager instead of 
                                #  traditional models.Manager, allowing for make_stage while keeping
                                #  all the regular functionality

    def __unicode__(self):
        return u'Stage: ' + unicode(self.width) + u'x' + unicode(self.height) + u'; Owner: ' + unicode(self.owner) + u'\n' + unicode(self.data)

class BlockManager(models.Manager):
    @staticmethod
    def build_default(): # Call Block.objects.build_default() if there are no blocks yet
        if len(Block.objects.filter(ID = '#')) == 0:
            Block(ID = '#', sprite = 'images/Block.gif').save()
        if len(Block.objects.filter(ID = Block.startID)) == 0:
            Block(ID = Block.startID, sprite = 'images/Kirby.gif').save()
        if len(Block.objects.filter(ID = Block.endID)) == 0:
            Block(ID = Block.endID, sprite = 'images/Chest.gif').save()

class Block(models.Model):
    """
        We will mostly be editing this one ourselves by hardcoding blocks.
        If the time comes such that users can use custom sprites, we will
    need to change this such that it keeps track of the Stage it's attached
    to so that a custom sprite can be loaded per stage. Until then, all
    stages will have the same spriteset.
    """
    startID = 'S'
    endID = 'E'
    ID = models.CharField(max_length = 1, primary_key = True)
    sprite = models.URLField()
    objects = BlockManager()

    def __unicode__(self):
        return unicode(self.ID) + u': ' + unicode(self.sprite)

class StageModel:

    def __init__(self):
        print "StageModel initiated"

    def render(self, width, height, data, owner):
        print "rendering stage!"
        rendered_stage = Stage.objects.make_stage(width, height, data, owner)
        rendered_stage.save()
        return rendered_stage.pk

pdm_stages = StageModel()
