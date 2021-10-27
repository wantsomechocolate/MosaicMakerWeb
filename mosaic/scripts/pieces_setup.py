import os, sys


sys.path.append("\\".join(os.getcwd().split('\\')[0:-3]))
from MosaicMaker import mosaic_maker as mm

arg_list = ['丽江古城','云南蘑菇火锅','张家界','玉龙雪山','腾冲','西双版纳','香格里拉']

for arg in arg_list:

    #arg = "Yunnan"

    piece_list_directory_base = r'C:\Users\JamesM\Projects\Programming\MosaicMakerImages\zzSearchQueries'

    piece_list_directory = os.path.join(piece_list_directory_base,arg)

    piece_list = mm.PieceList( piece_list_directory )
    tag_name = os.path.basename(piece_list_directory)

    from io import BytesIO
    from django.core.files.uploadedfile import InMemoryUploadedFile

    import django

    sys.path.append('C:/Users/JamesM/Projects/Programming/MosaicMakerWeb/mosaicweb')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'mosaicweb.settings'
    django.setup()

    from mosaic.models import Piece, Tag


    tag = Tag.objects.filter(name = tag_name).first()
    if tag == None:
        tag = Tag(name = tag_name)
        tag.save()
        

    for i in range(len(piece_list.pieces)):

        img_io = BytesIO()
        img_to_save = piece_list.pieces[i].img
        img_to_save.save(img_io,format = piece_list.pieces[i].original_image.format)
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
        piece.tags.set([tag])
