import os, sys
sys.path.append("\\".join(os.getcwd().split('\\')[0:-1]))

from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse

from MosaicMaker import mosaic_maker


def index(request):
    return HttpResponse("Hello, world. You're at the polls index. Made a change")

#def mosaic_view(request, mosaic_name):
#	return HttpResponse("Hello, you're trying to view: " + mosaic_name)

def mosaic_detail(request,mosaic_name):
	context = { 'mosaic_name':mosaic_name,
				'filenames': [	['landscape/0-0.png','landscape/0-1.png','landscape/0-2.png'],
								['landscape/1-0.png','landscape/1-1.png','landscape/1-2.png'],
								['landscape/2-0.png','landscape/2-1.png','landscape/2-2.png'], 	] 	}

	master = Mosaic()
	master.grid=[[],[]]

	return render(request, "mosaic_detail.html", context)