from .models import Fish, Partner
from rest_framework import serializers

class FishSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Fish
		fields = ('name', 'active', 'created')

class PartnerSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Partner
		fields = ('deal_id', 'title', 'title_short', 'price', 'full_price', 
			 	  'discount', 'economy', 'bought', 'timeout', 'lat', 'lon',
			 	  'address', 'schedule', 'image_url')

	