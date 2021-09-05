from region.serilizer import RegionSerilizer
from region.models import Region
from region.views import region
from rest_framework import fields, serializers
from state.models import State
from region.serilizer import RegionSerilizer
from country.models import Region 

class StateSerilizer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['id','country','name','pincode','is_deleted',]

    # def to_representation(self, instance):
    #     rep = super().to_representation(instance)
    #     rep['region'] = RegionSerilizer(instance.region).data
    #     return rep