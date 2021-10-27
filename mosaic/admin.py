from django.contrib import admin
from mosaic.models import Mosaic, Piece, Section, Tag, Target

# Register your models here.
class MosaicAdmin(admin.ModelAdmin):
	list_display = ("title", "target", "granularity", "neighborhood_size", "fineness", "random_max", "rgb_weighting")

class PieceAdmin(admin.ModelAdmin):
	#list_display = ("img","mode")
	pass

class SectionAdmin(admin.ModelAdmin):
	list_display = ("coordinate_w", "coordinate_h", "pinned", "priority", "mosaic", "piece")

class TagAdmin(admin.ModelAdmin):
	list_display = ("id","name",)

class TargetAdmin(admin.ModelAdmin):
	list_display = ("id","img",)


admin.site.register(Mosaic, MosaicAdmin)
admin.site.register(Piece, PieceAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Target, TargetAdmin)