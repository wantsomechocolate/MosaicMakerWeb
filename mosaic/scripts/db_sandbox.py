import os, sys
sys.path.append("\\".join(os.getcwd().split('\\')[0:-3]))
from MosaicMaker import mosaic_maker as mm

import django
sys.path.append('C:/Users/JamesM/Projects/Programming/MosaicMakerWeb/mosaicweb')
os.environ['DJANGO_SETTINGS_MODULE'] = 'mosaicweb.settings'
django.setup()
from mosaic.models import Mosaic, Section, Piece, Tag


#tags = Tag.objects.filter(name = "AnqiBW1")
