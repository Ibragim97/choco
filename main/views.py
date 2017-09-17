# -*- coding: utf-8 -*-
from __future__ import unicode_literals


import json

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.shortcuts import render
from django.http import JsonResponse

from rest_framework import viewsets
from rest_framework import permissions

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


from .serializers import FishSerializer, PartnerSerializer
from .models import Fish, User, Partner, Counter, CounterTotal
from .utils import getPartners



@method_decorator(csrf_exempt, name='dispatch')
class ApiGetView(View):
    def get(self, request):
        return JsonResponse({'status': 'error', 'data': 'Hello world'})

    def post(self, request):
        results = []

        data = request.body
        print data
        
        try:
            d = json.loads(data)
            lat = float(d['lat'])
            lon = float(d['lon'])
            token = d['token']

            # print lat
            # print lon  
            # print token 
        except:
            print "Wrong Json format!"
        else:
            try:
                user = User.objects.get(token=token)
            except:
                user = User(token=token)
                user.save()

            # lat = 43.200871
            # lon = 76.892258

            partners = getPartners(lat, lon, user)
            
        
            for p in partners:
                print p.deal_id
                print p.title
                # print "\n"
                # partner will not be suggested next time
                user.partners.add(p)
                serializer = PartnerSerializer(p)
                ser_data = serializer.data
                if p.subcategory:
                    ser_data['subcategory'] = p.subcategory.subcategoryName
                    ser_data['category'] = p.subcategory.category.categoryName
                results.append(ser_data)

        return JsonResponse({'results': results})


@method_decorator(csrf_exempt, name='dispatch')
class ApiUpdateView(View):
    def get(self, request):
        return JsonResponse({'data': 'It is update'})

    def post(self, request):
        results = []

        data = request.body
        
        try:
            d = json.loads(data)
            token = d['token']
            deal_id = int(d['deal_id'])

            print token
            print deal_id

            subcategory = Partner.objects.get(deal_id=deal_id).subcategory
            
            # print subcategory.subcategoryName

        except:
            print "Wrong data!"
        else:
            try:
                user = User.objects.get(token=token)
            except:
                user = User(token=token)
                user.save()

            if subcategory != None:
                category = subcategory.category
                try:
                    m1 = Counter.objects.get(user=user, subcategory=subcategory)
                except:
                    m1 = Counter(user=user, subcategory=subcategory)
                try:
                    m2 = CounterTotal.objects.get(user=user, category=category)
                except:
                    m2 = CounterTotal(user=user, category=category)
                m1.counter += 1
                m2.counter += 1
                # print category.categoryName
                # print subcategory.subcategoryName
                # print m1.counter
                # print m2.counter
                m1.save()
                m2.save()

        return JsonResponse({'status': 'OK'})



class FishViewSet(viewsets.ModelViewSet):
    queryset = Fish.objects.all()
    serializer_class = FishSerializer

