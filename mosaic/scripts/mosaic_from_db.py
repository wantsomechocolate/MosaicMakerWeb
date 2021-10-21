import os, sys
sys.path.append("\\".join(os.getcwd().split('\\')[0:-3]))
from MosaicMaker import mosaic_maker as mm

import django
sys.path.append('C:/Users/JamesM/Projects/Programming/MosaicMakerWeb/mosaicweb')
os.environ['DJANGO_SETTINGS_MODULE'] = 'mosaicweb.settings'
django.setup()
from mosaic.models import Piece

piece_list = mm.PieceList(list(Piece.objects.all()))



master = mm.Mosaic(r'C:\Users\JamesM\Projects\Programming\MosaicMakerImages\Anqi\BWSmile\BWSmile.png', granularity=1/16)
master.create(piece_list)

#master.output_html()

master.title = "Test Mosaic"
record = dict(title = master.title,
              granularity = master.granularity,
              neighborhood_size = master.neighborhood_size,
              fineness = master.f,
              random_max = master.random_max,
              w_sections = master.w_sections,
              h_sections = master.h_sections,
              rgb_weighting = master.rgb_weighting,
              opts = {},
              )

from mosaic.models import Mosaic
new_mosaic = Mosaic(**record)
new_mosaic.save()


## Now to loop through all the sections in the mosaic and add a record to the section table with a reference to the mosaic and to the piece, then I can build the mosaic in a view!!!!!!!!!


from mosaic.models import Section

for i in range(len(master.grid)):
    for j in range(len(master.grid[i])):
        section = dict(coordinate_h = master.grid[i][j].coordinates[0],
                    coordinate_w = master.grid[i][j].coordinates[1],
                    coordinates = master.grid[i][j].coordinates,
                    height = master.grid[i][j].height,
                    width = master.grid[i][j].width,
                    pinned = False,
                    priority = 0,
                    mosaic = new_mosaic,
                    piece = master.grid[i][j].piece.original_object,)

        new_section = Section(**section)
        new_section.save()
