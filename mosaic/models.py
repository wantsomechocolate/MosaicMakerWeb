from django.db import models

# Create your models here.

class Tag(models.Model):
	name = models.CharField(max_length=100)


class Piece(models.Model):
    img = models.ImageField(upload_to ='mosaic/pieces/')
    mode = models.CharField(max_length=20)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tag', related_name='pieces', blank=True)



class Mosaic(models.Model):

	title = models.CharField(max_length=255)
	
	#Perhaps this should be a reference so that base images can be stored in their own table?
	#one argument for this is that many mosaics can use the same base image, but one mosaic can't use multiple base images.  
	# set blank=True for this one while I decide. I don't neeeeeed it to set up the mosaic anyway. 
	base_img = models.ImageField(upload_to ='mosaic/base_images/', blank=True)

	granularity = models.IntegerField()
	neighborhood_size = models.IntegerField()
	fineness = models.IntegerField()
	random_max = models.IntegerField()
	w_sections = models.IntegerField()
	h_sections = models.IntegerField()

	## Just a simple array
	rgb_weighting = models.JSONField()

	## a grid containing information about all the sections in the mosaic.
	mosaic_grid_data = models.JSONField(blank = True, null = True)
	#	{ 	coordinates: [0,0],
	#		mode:'RGB',
	#		piece:id?,
	#		pinned:True/False
	#		priority: 10,
	#		height:100,
	#		width:200,			}

	opts = models.JSONField()

	## These should probably be references
	#comparison_function
	#reduce_function
	#error_function
	created_on = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True)

    ## Should have a user at some point




class Section(models.Model):

	coordinate_x = models.IntegerField()
	coordinate_y = models.IntegerField()

	## Not sure which one I want to use yet. 
	coordinates = models.JSONField()

	height = models.IntegerField()
	width  = models.IntegerField()

	pinned = models.BooleanField()
	priority = models.IntegerField()

	created_on = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True)
	mosaic = models.ForeignKey('Mosaic', on_delete=models.CASCADE)
	piece = models.ForeignKey('Piece', on_delete=models.SET_NULL, blank = True, null=True)

