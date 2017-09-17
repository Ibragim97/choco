# -*- coding: utf-8 -*-

import json 
import datetime
import requests
from math import sin, cos, sqrt, atan2, radians

from .models import Partner, Category, Subcategory, Counter, CounterTotal
from django.http import HttpResponse


def getSubcategory(id):
    url = 'https://chocolife.me/%d' % id
    page = requests.get(url).content

    subpage = page.split('e-subcategory__navigator--selected')[1]
    subpage = subpage.split('data-emarsysTitle')[1]
    subpage = subpage.split('"')[1]
    categoryName = subpage.split('>')[1]
    subcategoryName = subpage.split('>')[2]

    try:
        category = Category.objects.get(categoryName=categoryName)
    except:
        print "Category exception"
        category = Category(categoryName=categoryName)
        category.save()

    try:
        subcategory = Subcategory.objects.get(subcategoryName=subcategoryName)
    except:
        print "Subcategory exception"
        subcategory = Subcategory(category=category, subcategoryName=subcategoryName)
        subcategory.save()

    return subcategory


def parseJson():

    def convertDateTime(str):
        return datetime.datetime.strptime(str, '%Y-%m-%d %H:%M:%S')

    with open('deals.json') as json_file:
        data = json.load(json_file)['result']

        for obj in data:
            deal_id = obj.get('deal_id')
            title = obj.get('title')
            title_short = obj.get('title_short')
            price = obj.get('price')
            full_price = obj.get('full_price')
            discount = obj.get('discount')
            economy = obj.get('economy')
            bought = obj.get('bought')
            timeout = convertDateTime(obj.get('timeout'))
                      
            places = obj.get('places')
            if places:
                lat = places[0].get('lat')
                lon = places[0].get('lon')
                address = places[0].get('address')
                schedule = places[0].get('schedule')
                # phones = places[0].get('phones')

            plate_image_exists = obj.get('plate_image_exists')
            image_url = obj.get('image_url')

            try:
                partner = Partner.objects.get(deal_id=deal_id)
            except:
                try:
                    subcategory = getSubcategory(deal_id)
                except:
                    subcategory = None
                    print "Subcategory exception"

                partner = Partner(deal_id=deal_id, title=title, title_short=title_short, 
                                  price=price, full_price=full_price, discount=discount,
                                  economy=economy, bought=bought, timeout=timeout,
                                  lat=lat, lon=lon, address=address, schedule=schedule,
                                  plate_image_exists=plate_image_exists,
                                  image_url=image_url, subcategory=subcategory)

                partner.save()
                print "Partner added"

    return


def getPartners(lat, lon, user):

    def getDistance(a, b):
        R = 6373.0

        lat1 = radians(a[0])
        lon1 = radians(a[1])
        lat2 = radians(b[0])
        lon2 = radians(b[1])

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c * 1000
        return distance 

    results_near = []
    distances = []
    R = 1000
    partners = user.partners.all()
    # partners = []

    for p in Partner.objects.all():
        d = getDistance((lat, lon), (p.lat, p.lon))
        if (d < R) and (p not in partners):
            results_near.append(p)
            distances.append(d)

    print "length: %s" % len(results_near)

    first = []    # by subcategory and distance
    second = []   # by category and distance
    third = []    # by distance

    # print "First:"
    for p in results_near:
        try:
            m = Counter.objects.get(user=user, subcategory=p.subcategory)
            cnt = m.counter
            first.append((cnt, p)) 
        except:
            pass
    first.sort()
    # for f in first:
    #     print "%d %s %d" % (f[0], f[1].subcategory.subcategoryName, f[1].deal_id)
    # print "\n"
    first = [x[1] for x in first]

    # print "Second:"
    for p in results_near:
        try:
            
            m = CounterTotal.objects.get(user=user, category=p.subcategory.category)
            cnt = m.counter
            if p not in first:
                second.append((cnt, p)) 
                # print "%s %d %d" % (p.subcategory.category.categoryName, cnt, p.deal_id)
        except:
            cnt = 0
    # print "\n"
    second.sort()
    second = [x[1] for x in second]

    for p in results_near:
        if (p not in first) and (p not in second):
            ind = results_near.index(p)
            dist = distances[ind]
            third.append((dist, p))
    third.sort()

    # print first
    # print second
    # print third
    third = [x[1] for x in third]

    results = [x for x in first] + [x for x in second] + [x for x in third]

    return results[:5]