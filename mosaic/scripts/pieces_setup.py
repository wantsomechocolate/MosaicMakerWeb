import os, sys


sys.path.append("\\".join(os.getcwd().split('\\')[0:-3]))
from MosaicMaker import mosaic_maker as mm

piece_list_directory = r'C:\Users\JamesM\Projects\Programming\MosaicMakerImages\Anqi\BWSmile\BWSmile\html\html-1634365421\pieces'
piece_list = mm.PieceList( piece_list_directory )

from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

import django

sys.path.append('C:/Users/JamesM/Projects/Programming/MosaicMakerWeb/mosaicweb')
os.environ['DJANGO_SETTINGS_MODULE'] = 'mosaicweb.settings'
django.setup()

from mosaic.models import Piece

for i in range(len(piece_list.pieces)):

    img_io = BytesIO()
    img_to_save = piece_list.pieces[i].img
    img_to_save.save(img_io,format = img_to_save.format)
    img_to_save_filename = img_to_save.filename.split(os.path.sep)[-1]
    img_to_save_content_type = img_to_save.get_format_mimetype()
    img_in_memory = InMemoryUploadedFile(   img_io,	                # file
                                            None, 		        # fieldname?
                                            img_to_save_filename,       # file name
                                            img_to_save_content_type,   # content/type
                                            img_io.tell(), 	        # size
                                            None 		     )  # content type extra 


    piece = Piece(img = img_in_memory, mode = img_to_save.mode)
    piece.save()

