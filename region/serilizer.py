from rest_framework import fields, serializers
from region.models import Region

class RegionSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name','is_deleted',]
