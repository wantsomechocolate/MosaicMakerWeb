import os, sys
sys.path.append("\\".join(os.getcwd().split('\\')[0:-3]))
from MosaicMaker import mosaic_maker as mm

import django
sys.path.append('C:/Users/JamesM/Projects/Programming/MosaicMakerWeb/mosaicweb')
os.environ['DJANGO_SETTINGS_MODULE'] = 'mosaicweb.settings'
django.setup()
from mosaic.models import Piece,Tag,Mosaic,Target,Section

tags = Tag.objects.filter(name__in = ["香格里拉","西双版纳","腾冲","玉龙雪山","张家界","云南蘑菇火锅","丽江古城","Yunnan","Yangshuo","The Great Wall of China","Terracotta Army","Spring Festival","Shigu China","Lantern Festival","Harbin","China Nature Wallpaper","China"])
pieces = Piece.objects.filter(tags__in = tags)
piece_list = mm.PieceList(list(pieces),max_instances = 10)

target_img_path = r'C:\Users\JamesM\Projects\Programming\MosaicMakerImages\木子\AnqiMama1.jpg'
#target = Target(img = target_img_path)
#target.save()

target = Target(id=4)

master = mm.Mosaic(target_img_path, granularity=1/50, f=5, neighborhood_size = 5)
master.create(piece_list)

#master.output_html()

master.title = "Anqi Mama 1"
record = dict(title = master.title,
              target = target,
              granularity = master.granularity,
              neighborhood_size = master.neighborhood_size,
              fineness = master.f,
              random_max = master.random_max,
              #w_sections = master.w_sections,
              #h_sections = master.h_sections,
              rgb_weighting = master.rgb_weighting,
              opts = {},
              )

#from mosaic.models import Mosaic
new_mosaic = Mosaic(**record)
new_mosaic.save()


## Now to loop through all the sections in the mosaic and add a record to the section table with a reference to the mosaic and to the piece, then I can build the mosaic in a view!!!!!!!!!


#from mosaic.models import Section

for i in range(len(master.grid)):
    for j in range(len(master.grid[i])):
        section = dict(coordinate_h = master.grid[i][j].coordinates[0],
                    coordinate_w = master.grid[i][j].coordinates[1],
                    #coordinates = master.grid[i][j].coordinates,
                    #height = master.grid[i][j].height,
                    #width = master.grid[i][j].width,
                    pinned = False,
                    priority = 0,
                    mosaic = new_mosaic,
                    piece = master.grid[i][j].piece.original_object,)

        new_section = Section(**section)
        new_section.save()
