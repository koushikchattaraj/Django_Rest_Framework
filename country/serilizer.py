from django.db.models.fields.related import RECURSIVE_RELATIONSHIP_CONSTANT
from region.serilizer import RegionSerilizer
from region.models import Region
from region.views import region
from rest_framework import fields, serializers
from country.models import Country
from region.serilizer import RegionSerilizer
from region.models import Region 

class CountrySerilizer(serializers.ModelSerializer):
    # region = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # print(region)
    region = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Country
        fields = ['id','region','name','country_code','is_deleted']
    def get_region(self, obj):
        region_name = obj.region.name
        return region_name

