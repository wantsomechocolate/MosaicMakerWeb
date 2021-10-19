from django.contrib import admin
from mosaic.models import Mosaic, Piece, Section, Tag

# Register your models here.
class MosaicAdmin(admin.ModelAdmin):
    pass

class PieceAdmin(admin.ModelAdmin):
	pass

class SectionAdmin(admin.ModelAdmin):
	pass

class TagAdmin(admin.ModelAdmin):
	pass


admin.site.register(Mosaic, MosaicAdmin)
admin.site.register(Piece, PieceAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Tag, TagAdmin)