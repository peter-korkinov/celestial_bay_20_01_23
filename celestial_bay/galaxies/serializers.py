from rest_flex_fields import FlexFieldsModelSerializer
from versatileimagefield.serializers import VersatileImageFieldSerializer

from .models import Constellation, ConstellationImage, Galaxy, GalaxyImage,\
    Post, PostImage, Comment


class ConstellationSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Constellation
        fields = ['name', 'abbreviation', 'area_in_sq_deg']


class ConstellationImageSerializer(FlexFieldsModelSerializer):
    image = VersatileImageFieldSerializer(sizes='image_headshot')

    class Meta:
        model = ConstellationImage
        fields = ['pk', 'constellation', 'image']
