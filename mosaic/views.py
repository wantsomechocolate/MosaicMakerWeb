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


## Get the mosaic by the id (For now)
## Get all the sections associated with that mosaic
## Get the pieces associated with those sections
## send all that to the view? (should probably send the minimim amount of info required.)
## context = dict(mosaic = mosaic, sections = sections, pieces = pieces)

def mosaic_detail(request,mosaic_name):
	
	from PIL import Image

	mosaic_id = int(mosaic_name)
	mosaic_record = Mosaic.objects.filter(id = mosaic_id).first()

	target_image = Image.open(mosaic_record.target.img)

	master = mm.Mosaic( target_image, f = mosaic_record.fineness, granularity = mosaic_record.granularity )

	mosaic = mosaic_record #Mosaic.objects.filter(id=3)[0]
	mosaic.h_sections = master.h_sections
	mosaic.w_sections = master.w_sections
	mosaic.h_range = range(master.h_sections)
	mosaic.w_range = range(master.w_sections)
	sections = Section.objects.filter(mosaic = mosaic.id)

	pieces = []
	for section in sections:
	    pieces.append(section.piece)
	pieces = list(set(pieces))



	#context = { 'mosaic_name':mosaic_name,
	#			'filenames': [	['landscape/0-0.png','landscape/0-1.png','landscape/0-2.png'],
	#							['landscape/1-0.png','landscape/1-1.png','landscape/1-2.png'],
	#							['landscape/2-0.png','landscape/2-1.png','landscape/2-2.png'], 	] 	}

	pieces_array = [(h,[None for w in range(mosaic.w_sections)]) for h in range(mosaic.h_sections)]
	for section in sections:
		try:
			pieces_array[section.coordinate_h][1][section.coordinate_w] = (section.coordinate_h,section.coordinate_w,section.piece.img.url)
		except:
			print(section.h_sections,section.w_sections)

	context = dict(mosaic = mosaic, sections = sections, pieces = pieces, pieces_array = pieces_array)

	return render(request, "mosaic_detail.html", context)