from django.contrib import admin
from CropRecommendationApp.models import *

# Register your models here.

admin.site.register(crop)
admin.site.register(crop_recommed)
admin.site.register(Fertilizer)
admin.site.register(fertilizer_recommed)

admin.site.site_header = 'AGRICROP'
admin.site.site_title = 'AGRICROP'
admin.site.index_title = 'Administrator'