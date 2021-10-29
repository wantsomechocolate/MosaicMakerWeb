import os, sys
sys.path.append("\\".join(os.getcwd().split('\\')[0:-1]))

from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse

from MosaicMaker import mosaic_maker as mm
from .models import Mosaic,Piece,Section,Tag,Target


def mosaic_index(request):
	context = dict()
	return render(request, "mosaic_detail.html", context)

#def mosaic_view(request, mosaic_name):
#	return HttpResponse("Hello, you're trying to view: " + mosaic_name)




## Get the mosaic by the id (For now, will eventually switch that to the name using underscores)
## Get all the sections associated with that mosaic
## Get the pieces associated with those sections
## send all that to the view? (should probably send the minimim amount of info required.)
## context = dict(mosaic = mosaic, sections = sections, pieces = pieces)

## What I really need is a standardized way to go from db entry to mosaic object
## Like, I even think I'd like to have the pieces assigned to the proper sections on the mosaic object itself, would that be useful? 
## because this object needs to persist in the cache or whatever, right? I mean, at least new ones need to

def mosaic_db_to_object(mosaic_id):
	from PIL import Image
	mosaic_record = Mosaic.objects.filter(id = mosaic_id).first()
	if mosaic_record == None:
		print("id:",mosaic_id," doesn't exist")
		return None

	target_image = Image.open(mosaic_record.target.img)

	master = mm.Mosaic( target_image, 
						granularity 			= mosaic_record.granularity 		, 
	
						#comparison_function 	= mosaic_record.cf					,
						#reduce_function 		= mosaic_record.rf 					,
						#error_function 		= mosaic_record.ef					,

						f 						= mosaic_record.fineness 			,
						rgb_weighting 			= mosaic_record.rgb_weighting 	 	, 
						random_max 				= mosaic_record.random_max 			, 
						neighborhood_size 		= mosaic_record.neighborhood_size 	, 
		
						opts 					= mosaic_record.opts 				, 	)


	master.title = mosaic_record.title

	## Then I need to go through all the sections in the database, make sure the number of sections matches the
	## number of expected sections
	## Then I need to add any properties of the sections to the mosaic object, right? I should do that and it's not a waste of time?

	sections = Section.objects.filter(mosaic = mosaic_record.id)
	
	## I can actually go through all sections and see what the overall dimensions are expected to be and compare them
	## Can I get the granularity in the reverse way? If have the number of dimensions (take smaller of w_sections and h_sections)
	## then just 1 over that? I think I'll run into some rounding issues. when I use 1/50 sometimes I end up with 53
	## forget this for now, assume no one is tinkering with the granularity of already created mosaic (yeah right!)
	## I might have to do something like fetch a mosaic based on uniqueness of user, target image, and granularity or something. 

	#if (section_peak_h,section_peak_w) == (master.h_sections, master.w_sections):
	for section in sections:
		## This should also be a seperate function section_db_to_object
		grid_section = master.grid[section.coordinate_h][section.coordinate_w]
		grid_section.pinned = section.pinned
		grid_section.priority = section.priority

		## I can't just do this because the piece needs to be a mosaic image object
		#grid_section.piece = section.piece

		## So I need another function piece_db_to_object, is there a reason to pass the tags here? for now I'll say
		## that's only useful when fetching pieces to use in the first place, I can add it later, but I don't need it right now. 
		## do I want to use the picelist object with a list and one piece as the argument? would that take 1000 years?
		## I like the idea for the future in case I decide to save multiple pieces for each section?
		## I have already modified piece list to handle a list of db objects (pretty dirtily though, but I guess I'll use it at the moment)
		## Also the piece db to object funtion needs to set default_save_size and max_instances, these might be better saved on the mosaic instance and then
		## passed on?
		piece = mm.PieceList([section.piece]).pieces[0]
		grid_section.piece = piece
		grid_section.piece.img.close()

	#else:
		#print("Mosiac granularity doesn't match sections, creating new mosaic in database with same target")
		#if using new sections that you can just skip this part!	

	return master

def piece_array_from_mosaic_id(mosaic_id):
	mosaic_record = Mosaic.objects.filter(id = mosaic_id).first()
	mosaic_sections = Section.objects.filter(mosaic = mosaic_record.id)
	#mosaic_pieces = Piece.objects.filter(section__in = mosaic_sections)


def mosaic_detail(request,mosaic_name):
	
	from PIL import Image

	mosaic_id = int(mosaic_name)
	#master = mosaic_db_to_object(mosaic_id)
	#target_image = master.target.img

	mosaic_record = Mosaic.objects.filter(id = mosaic_id).first()
	target_image = Image.open(mosaic_record.target.img)

	master = mm.Mosaic( target_image, f = mosaic_record.fineness, granularity = mosaic_record.granularity )

	#mosaic = mosaic_record #Mosaic.objects.filter(id=3)[0]
	#mosaic.h_sections = master.h_sections
	#mosaic.w_sections = master.w_sections
	#mosaic.h_range = range(master.h_sections)
	#mosaic.w_range = range(master.w_sections)
	sections = Section.objects.filter(mosaic = mosaic_record)

	#pieces = []
	#for section in sections:
	#    pieces.append(section.piece)
	#pieces = list(set(pieces))



	#context = { 'mosaic_name':mosaic_name,
	#			'filenames': [	['landscape/0-0.png','landscape/0-1.png','landscape/0-2.png'],
	#							['landscape/1-0.png','landscape/1-1.png','landscape/1-2.png'],
	#							['landscape/2-0.png','landscape/2-1.png','landscape/2-2.png'], 	] 	}

	pieces_array = [(h,[None for w in range(master.w_sections)]) for h in range(master.h_sections)]
	for section in sections:
	#	try:
		pieces_array[section.coordinate_h][1][section.coordinate_w] = (section.coordinate_h,section.coordinate_w,section.piece.img.url)
	#	except:
	#		print(section.h_sections,section.w_sections)

	#for h in range(master.h_sections):
	#	for w in range(master.w_sections):
	#		pieces_array[h][1][w] = (h,w,master.grid[h][w].piece.original_object.img.url)

	context = dict(pieces_array = pieces_array) #, sections = sections, pieces = pieces, ) mosaic = master, 

	return render(request, "mosaic_detail.html", context)

