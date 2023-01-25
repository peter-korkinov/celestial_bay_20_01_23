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


class GalaxySerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Galaxy
        fields = ['pk', 'name', 'name_origin', 'notes', 'galaxy_type', 'distance',
                  'apparent_magnitude', 'size', 'owner', 'constellation']
        expandable_fields = {
            'images': ('galaxies.GalaxyImageSerializer', {'many': True}),
        }


class GalaxyImageSerializer(FlexFieldsModelSerializer):
    image = VersatileImageFieldSerializer(sizes='image_headshot')

    class Meta:
        model = GalaxyImage
        fields = ['pk', 'galaxy', 'image']
