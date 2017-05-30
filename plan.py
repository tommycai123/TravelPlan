import random
import copy
from pandas.tseries.offsets import Hour,Minute
import pandas as pd
from  datetime import datetime
distance = [[0 for i in xrange(4)] for j in xrange(4)]
tracks = []
goods = []
format = '%Y/%m/%D %H:%M'
with open("input/road.csv") as f:
    for index,i in enumerate(f):
        if index==0:
            continue
        t= str(i).split(",")
        distance[int(t[0])-1][int(t[1])-1]=int(t[2])

class Tracker(object):
    def __init__(self,lines):
        self.start = int(lines.start)
        self.end = int(lines.end)
        self.volume = float(lines.volume)
        self.weight = float(lines.weight)
        self.speed = float(lines.speed)
        self.cost_day = float(lines.cost_day)
        self.cost_dis = float(lines.cost_dis)
        self.status = 0 #0 表示处于接单状态,1表示处于不接单状态
        self.good = None
        self.get_time=None
        self.arrive_time =None
        self.current_city =self.start
        self.cost_this_traval =0
        self.assign_next=0
    def durtimeCal(self,start,end):
        during=distance[start][end]/self.speed
        t2 = Hour(int(during))+Minute(60*(during-int(during)))
        return t2
    def duringTime(self,time1,time2):
        if type(time1)==datetime:
            t= (time2-time1).total_seconds()/3600
        else:
            t= (datetime.strptime(time2,format=format)-datetime.strptime(time1,format=format)).total_seconds()/3600
        return t
    def evaluate(self,get_time,good):
        self.update(get_time)
        during = self.durtimeCal(good.start,good.end)
        if self.status ==1:
            tunning_time =self.durtimeCal(self.current_city,good.start)
            go = self.arrive_time+Minute(20) +tunning_time
            arrival = go +Minute(20) + during
            cost = self.cost_dis*(self.duringTime(go,arrival) + tunning_time.total_seconds()/3600 + self.durtimeCal(good.end,self.end))
            + self.cost_day*(self.duringTime(go,
        else:
            tunning_time = self.durtimeCal(self.current_city,good.start)
            go = get_time+tunning_time
            arrival =get_time+ Minute(20) + tunning_time +during
            cost = self.duringTime(go,arrival) +
        return go, arrival
    def assign(self,good,get_time,arrival_time):
        self.status =1
        self.good = good
        self.get_time = get_time
        self.arrive_time = arrival_time
    def update(self,time):
        if self.status ==1:
            if time>self.arrive_time + Minute(20):
                self.status = 0
        else:
            self.status =0


class Goods(object):
    def __init__(self,lines):
        self.start = int(lines.start)
        self.end = int(lines.end)
        self.volume = float(lines.volume)
        self.weight = float(lines.weight)
        self.t1 = lines.t1
        self.t2 = lines.t2

def solve():
    a = pd.read_csv("input/vehicle.csv")
    length, width = a.shape
    number_trackers = length
    for i in xrange(length):
        tracks = Tracker(a.ix[i])
    b = pd.read_csv("input/goods.csv")
    length, width = b.shape
    number_goods = length
    for i in xrange(length):
        goods = Goods(b.ix[i])

if __name__ =="__main__":
    solve()