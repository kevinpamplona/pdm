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
    def make_stage(w, h, stagename, dat, user):
        if w <= 0 or h <= 0 or w*h > Stage.MAX_SIZE:
            raise FieldError("Invalid width or height")

        return Stage(width = w, height = h, name = stagename, data = dat, rating = 1, owner = user)

    @staticmethod
    def default_stage():
        return Stage(
            width = 11,
            height = 5,
            name = 'rainbow road',
            data = DEFAULT,
            rating = 0,
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
    name     = models.CharField(max_length = 255)
    data     = models.CharField(max_length = MAX_SIZE)
    owner    = models.CharField(max_length = 255)
    rating   = models.SmallIntegerField(default = 0)
    objects  = StageManager()   # Redirects Stage.objects to be the custom StageManager instead of 
                                #  traditional models.Manager, allowing for make_stage while keeping
                                #  all the regular functionality

    def __unicode__(self):
        return u'Stage: ' + unicode(self.name) + u'--' + unicode(self.width) + u'x' + unicode(self.height) + u'; Owner: ' + unicode(self.owner) + u', Rating: ' + unicode(self.rating) + u'\n' + unicode(self.data)

class BlockManager(models.Manager):
    @staticmethod
    def build_default(): # Call Block.objects.build_default() if there are no blocks yet
        if len(Block.objects.filter(ID = '#')) == 0:
            Block(ID = '#', sprite = 'images/Block.gif').save()
        if len(Block.objects.filter(ID = Block.startID)) == 0:
            Block(ID = Block.startID, sprite = 'images/Kirby.gif').save()
        if len(Block.objects.filter(ID = Block.endID)) == 0:
            Block(ID = Block.endID, sprite = 'images/Chest.gif').save()
        if len(Block.objects.filter(ID = 'x')) == 0:
            Block(ID = 'x', sprite = 'images/Enemy.gif').save()

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

    def render(self, width, height, name, data, owner):
        #print "rendering stage!"
        rendered_stage = Stage.objects.make_stage(width, height, name, data, owner)
        #print rendered_stage
        rendered_stage.save()
        #print rendered_stage.pk
        return rendered_stage.pk

    def upvote(self, stageid):
        # upvote stage
        stage = Stage.objects.get(pk=stageid)
        new_rating = stage.rating + 1
        stage.rating = new_rating
        stage.save()
        return stage.rating

    def downvote(self, stageid):
        # downvote stage
        stage = Stage.objects.get(pk=stageid)
        new_rating = stage.rating - 1
        stage.rating = new_rating
        stage.save()
        return stage.rating

pdm_stages = StageModel()
