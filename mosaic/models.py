from django.db import models

# Create your models here.

class Tag(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return f"{self.id}: {self.name}"

class Piece(models.Model):
	img = models.ImageField(upload_to ='mosaic/pieces/')
	## Having second thoughts about saving this guy, 
	## I can just get it from the img object after I obtain it, the only reason to save it is if I'll ever filter by it, but why would I do that?
	mode = models.CharField(max_length=20) 
	created_on = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True)
	tags = models.ManyToManyField('Tag', related_name='pieces', blank=True)

	#def __str__(self):
	#	return f"{self.id}:, {self.mode}, {self.tags}, {self.created_on}, {self.last_modified}"

class Target(models.Model):
	img = models.ImageField(upload_to = 'mosaic/targets/')
	created_on = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True)

def rgb_weighting_default():
	return [1,1,1]


## I need to add the comparison function, error function, and reduce function arguments to this model at some point in the phewture
class Mosaic(models.Model):

	title = models.CharField(max_length=255)
	
	#Perhaps this should be a reference so that base images can be stored in their own table?
	#one argument for this is that many mosaics can use the same base image, but one mosaic can't use multiple base images.  
	# set blank=True for this one while I decide. I don't neeeeeed it to set up the mosaic anyway. 
	#base_img = models.ImageField(upload_to ='mosaic/base_images/', blank=True)
	target = models.ForeignKey('Target', on_delete=models.SET_NULL, blank = True, null=True)

	granularity = models.FloatField(default = 1/16)
	neighborhood_size = models.IntegerField(default = 1)
	fineness = models.IntegerField(default = 2)
	random_max = models.IntegerField(default = 0)

	#these are calculated based on the granularity, I shouldn't save them independently. 
	#w_sections = models.IntegerField()
	#h_sections = models.IntegerField()

	## Just a simple array
	rgb_weighting = models.JSONField(default = rgb_weighting_default())

	## a grid containing information about all the sections in the mosaic.
	mosaic_grid_data = models.JSONField(blank = True, null = True)
	#	{ 	coordinates: [0,0],
	#		mode:'RGB',
	#		piece:id?,
	#		pinned:True/False
	#		priority: 10,
	#		height:100,
	#		width:200,			}

	## I might need to save some stuff about pieces here?
	# default_save_size = models.JSONField(default = (512,512))
	# max_instances = models.IntegerField(default = 5)

	opts = models.JSONField(blank = True, null = True)

	## These should probably be references
	#comparison_function
	#reduce_function
	#error_function
	created_on = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True)

    ## Should have a user at some point




class Section(models.Model):

	coordinate_w = models.IntegerField()
	coordinate_h = models.IntegerField()

	## Not sure which one I want to use yet. 
	#coordinates = models.JSONField()

	## I don't need to save this, it get's calculated on init
	#height = models.IntegerField()
	#width  = models.IntegerField()

	pinned = models.BooleanField()
	priority = models.IntegerField()

	mosaic = models.ForeignKey('Mosaic', on_delete=models.CASCADE)
	piece = models.ForeignKey('Piece', on_delete=models.SET_NULL, blank = True, null=True)

	created_on = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True)