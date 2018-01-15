# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.utils.safestring import mark_safe
from django import forms
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from datetime import datetime
from data.models import record
from django.views.decorators.csrf import csrf_exempt
import json
import codecs
from django.utils.encoding import uri_to_iri
from ctypes import*
from math import radians, cos, sin, asin, sqrt
from django.http import HttpResponse
import os
from django.template import Context, loader
from django import forms
import urlparse

from django.shortcuts import redirect

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

def hello_world(request):
    return HttpResponse("Hello World!")

def home_page(request):
    #fp = open('\users\djangouser\templates\mytemplate.html')
    #template = loader.get_template("/home/hello/djangogirls/testing/templates/temple_index/index.html")
    #return HttpResponse(template.render())
    b = request;
    print b;
    return render(request, 'index.html')

def get_data(request):
    #fp = open('\users\djangouser\templates\mytemplate.html')
    #template = loader.get_template("/home/hello/djangogirls/testing/templates/temple_index/index.html")
    #return HttpResponse(template.render())
    return render(request, 'getDataList.html')

def type_data(request):
    type = request.GET['type']
    if(type == 'data'):
        return render(request, 'typeData.html')
    elif(type == 'cell'):
        return render(request, 'typeCell.html')
    elif(type == 'handover'):
        return render(request, 'typeHandover.html')
    elif(type == 'call'):
        return render(request, 'typeCall.html')
    elif(type == 'movetype'):
        return render(request, 'typeMovetype.html')
    else:
        return render(request, 'getDataList.html')

def get_statictics(request):
    return render(request, 'statisticsPage.html')

def statisticsSelect(request):
    type = request.GET['type']
    if(type == 'all'):
        return redirect("http://140.113.216.37/signal/statisticsAll")
    elif(type == 'user'):
        return render(request,'statisticsUserSelect.html')
    elif(type == 'app'):
        return redirect("http://140.113.216.37/signal/statisticsApp")
    elif(type == 'appforday'):
        return redirect("http://140.113.216.37/signal/statisticsAppForDay")

    else:
        return render(request, 'staticticsPage.html')


def get_signalmap(request):
    return render(request, 'getSignalMap.html')

class user(Structure):
    _fields_ =[("h",c_int),("m",c_int),("s",c_int),("lon",c_float),("lat",c_float),("state",c_int)]
#state 1 for match
class location(Structure):
    _fields_ =[("lat",c_double),("lon",c_double)]

#caculate the distance
def haversine(lon1, lat1, lon2, lat2): # 经度1，纬度1，经度2，纬度2 （十进制度数）

    #Calculate the great circle distance between two points
    #on the earth (specified in decimal degrees)

    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # 地球平均半径，单位为公里
    return c * r * 1000
# print the gps in the database into a text file
def database_info(request):
    file = open('inter','a+')
    roads = record.objects.all()
    for road in roads:
        #print "let's do it"
        r_data = str(road.lat) + ' ' + str(road.lon) + '\n'
        file.write(r_data)
    file.close() # 關閉檔案

def user_info(request):
    path = []
    path.append('/home/hello/siginal/tapei_to_shinju/label0126')
    path.append('/home/hello/siginal/tapei_to_shinju/label0217')

    path_name = []
    path_name.append('label0126')
    path_name.append('label0217')

    #point = [16,15,14,13,12,11,10,9,8,7,6,5,4]
    point = [6,10,12,14]

    global s,count, result, min_d
    count = 0
    s = 0
    result = 0

    for point_cnt in range(0,len(point)):
        print('Calculate ' + str(point[point_cnt]) + ':\n')

        for path_cnt in range(0,len(path)):
                print('Runing ' + path[path_cnt] + '\n')

                for filename in os.listdir(path[path_cnt]):
                    print(filename)
                    data = json.loads(open(path[path_cnt] + '/' + filename).read())
                    #data = json.loads(open(path + '/' + 'label_CM0008RECORD201701260949').read())
                    for i in range(len(data)):
                        if 'Lat' in data[i] and data[i]['Lat'] != 'null' and data[i]['Lng'] != 'null' and data[i]['TimeStamp'] != 'null':
                            try:
                                msg = user(int(data[i]['TimeStamp'][11:13]),int(data[i]['TimeStamp'][14:16]),int(data[i]['TimeStamp'][17:19]),float(data[i]['Lng']),float(data[i]['Lat']),0)
                            except ValueError:
                                continue

                            # see the new data match or not
                            min_d = 10000000
                            roads = record.objects.all()
                            for road in roads:
                                distance = haversine(road.lon,road.lat, msg.lon,msg.lat)
                                if distance < 50:
                                    if distance < min_d:
                                        min_d = distance
                                else: continue

                            #save all the data blongs to that user into an array
                            lists = []
                            file = open( (data[i]['Account']+'_'+ str(point[point_cnt]) +'p'+  '_' + path_name[path_cnt]) ,'a+')
                            line = file.readline()
                            while line:
                                new_line = line.split()
                                #print new_line
                                info = user(int(new_line[0]),int(new_line[1]),int(new_line[2]),float(new_line[3]),float(new_line[4]),int(new_line[5]))
                                lists.append(info)
                                line = file.readline()

                            # state:
                            # 0->00 - don't match & not on the road
                            # 1->01 - don't match & on the road
                            # 2->10 - match & not on the road
                            # 3->11 - match & on the road
                            is_change = 0
                            if len(lists) < point[point_cnt]: # user's records less than 10
                                if min_d == 10000000 : # not match (so first bit of state is 0)
                                    if len(lists) == 0: # the first record write into the file
                                        msg.state = 0
                                    else:
                                        # see the state of the last record (on the road or not) new state = the state of the last record in the file
                                        if ( (lists[len(lists)-1].state == 0) or (lists[len(lists)-1].state == 2) ):
                                            msg.state = 0
                                        else:
                                            msg.state = 1
                                else: # match (so first bit of state is 1)
                                    if len(lists) == 0: # the first record write into the file
                                        msg.state = 2
                                    else:
                                        # see the state of the last record (on the road or not)
                                        if  ( (lists[len(lists)-1].state == 0 ) or (lists[len(lists)-1].state == 2) ):
                                            msg.state = 2 # not on the road
                                        else:
                                            msg.state = 3
                                result = "Not enough records"
                            else: # user's records more than 10
                                index = len(lists) - 1
                                if min_d == 10000000 : # not match (so first bit of state is 0)
                                    index = len(lists) - 1
                                    s = lists[index].state #state of the last records
                                    # ten records same = 11 -> 01; not same:road new state = last state 11->01
                                    if s == 3:
                                        msg.state = 1
                                    elif ( (s == 0) or (s == 2) ): # not on the road
                                         # ten records = 00 - > 00 ; 10 -> 00
                                         msg.state = 0
                                    else: # on the road (s = 01 not match & on the road)
                                        #initial it will change state
                                        flag = 1  #to make sure whether I should start to determine or not
                                        # to see the last ten state are same or not
                                        while index >= (len(lists) - point[point_cnt]) :
                                            if lists[index].state != s:
                                                flag = 0
                                                break
                                            index = index - 1

                                        if flag == 1: # ten reacords' state are same
                                            # ten records = 01 -> 00
                                            msg.state = 0
                                            is_change = 1
                                        else:
                                            msg.state = 1
                                else: # match
                                    index = len(lists) - 1
                                    s = lists[index].state #state of the last records
                                    if ( (s == 3) or (s == 1) ): # 11 -> match & on the road 01->don't match & on the road
                                        msg.state = 3 # match & on the road
                                    elif s == 0: # don't match & not on the road
                                        msg.state = 2 # match & not on the road
                                    else: # s == 10 match & not on the road
                                        flag = 1
                                        while index >= (len(lists) - point[point_cnt]) :
                                            if lists[index].state != s:
                                                flag = 0
                                                break
                                            index = index - 1
                                        if flag == 1: # ten reacords' state are same
                                            # ten records = 10 -> 11 match & on the road
                                            msg.state = 3
                                            is_change = 1
                                        else:
                                            msg.state = 2
                            new_data = str(msg.h) + ' ' + str(msg.m) + ' ' + str(msg.s) + ' ' + str(msg.lon) + ' ' + str(msg.lat)  + ' ' +  str(msg.state) + '\n'
                                #r_data = str(temp.lat)+ ' ' + str(temp.lon) + '\n'
                            file.write(new_data)
                            file.close() # 關閉檔案
                            #write the change data into the other file
                            if (is_change == 1):
                                file = open((data[i]['Account']+ '_change' + '_' + str(point[point_cnt]) + 'p'+ '_' + path_name[path_cnt]),'a+')
                                c = lists[len(lists) - 1]
                                change_data = str(c.h) + ' ' + str(c.m) + ' ' + str(c.s) + ' ' + str(c.lon) + ' ' + str(c.lat)  + ' ' +  str(c.state) + '\n'
                                file.write(change_data)
                                file.write(new_data)
                                file.close()


@csrf_exempt
def check(request):

    #jdata = json.loads(request.body.decode("utf-8"))
    if 'inter' in request.GET:
        result_temp=request.GET['inter']
        temp = uri_to_iri(result_temp)
        inter = temp.encode('utf8')
    #encoded = '%E5%9F%BA%E9%9A%86%E4%BA%A4%E6%B5%81%E9%81%93'
    #tmp_msg = uri_to_iri(encoded)
    #msg = tmp_msg.encode('utf8')
    return HttpResponse('Welcome!! This is your json data:'+str(inter))

@csrf_exempt
def test(request):
    #if request.method == 'POST':
    '''
    json_data="""
    [{ "no":"1000",
    "location":[
    {"lat":122.5, "lon" : 56.7},
    {"lat":124.5, "lon" : 55.7}
    ],
    "inter":
    }
    ]
    """
    '''
    jdata = json.loads(request.body.decode("utf-8"))
    #jdata = json.loads(json_data)
    for i in range(len(jdata)) :
        for j in range(len(jdata[i]['location'])):
            t_inter = jdata[i]['inter']
            tmp_msg = uri_to_iri(t_inter)
            inter = tmp_msg.encode('utf8')
            data = record.objects.create(
            lon=jdata[i]['location'][j]['lon'],
            lat=jdata[i]['location'][j]['lat'],
            no=jdata[i]['no'],
            inter=inter
            )
            data.save()

    return HttpResponse("Received Successfully.")
    #return HttpResponse("It was GET request.")

def filiter(request):
    data = record.objects.all()
    if 'no' in request.GET:
        result = data.filter(no=request.GET['no'])
        return render(request, 'records.html',{
            'result_lists': result
        })
    #data1.objects.all()

def mapp(request):
    data = record.objects.all()
    #result = data.objects.filiter(interchange='Hinchu')
    return render(request, 'map.html',{
        'result_lists': data
    })
def show(request):
    data = record.objects.all()
    #result = data.objects.filiter(interchange='Hinchu')
    return render(request, 'records.html',{
        'result_lists': data
    })

def delete_data(request):
    data = record.objects.all()
    if 'id' in request.GET:
        result = data.filter(id=request.GET['id'])
        result.delete()
    return HttpResponse("Delete Successfully.")
