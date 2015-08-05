# -*- coding: utf8 -*-

import re
import math
import datetime
from calendar import month
ORIGIN_DATE='20000101'
ORIGIN_YEAR='1980'


Directions={"东":6,"西":2,"南":8,"北":4,"东北":5,"东南":7,"西北":3,"西南":5}

def get_floor_name(string):
    if( string=='\N'):
        return 0
    elif(string.endswith('层')):
        try:
           return  int(string[0:-1])
        except Exception , e:
            return 0
    else :
        try:
            return int(string)
        except Exception ,e:
            return 0
        
def get_bedroom_amout(string):
    try :
        return int(string)
    except Exception,e:
        return 0
def get_parlor_amout(string):
    try :
        return int(string)
    except Exception,e:
        return 0
        
def get_toilet_amout(string):
    try :
        return int(string)
    except Exception,e:
        return 0        
def get_cookroom_amout(string):
    try :
        return int(string)
    except Exception,e:
        return 0 

def get_build_size(string):
    try:
        return float(string)
    except Exception,e:
        return 0
def get_face_code(string):
    if( string=='\N' or string==""):
        return 0
    ret=0
    splits=re.split(u';|,', string)
    scale=0.5
    for i in range(len(splits)):
        if(Directions.has_key(splits[i].strip()) ):
           ret+=Directions.get(splits[i].strip())*(math.pow(0.5, i))
           
    return ret
def  get_build_end_year(string):
    if(string=='\N'):
        return 0
    else:
        try:
            temp= int(string)-int(ORIGIN_YEAR)
            return temp
        except Exception,e:
            return 0
def get_is_sales_tax(string):
    
    if( string=='\N'):
        return 0
    else :
        try:
            return int(string)
        except Exception,e:
            return 0
        

def get_property_fee(string):
    if( string=='\N'):
        return 0
    else :
        try:
            return float(string)
        except Exception,e:
            return 0
def get_distance_metro_code (string):
    if( string=='\N'):
        return 0
    elif(string=='500400000600'):
        return 1
    elif(string=='500400000500'):
        return 2
    elif(string=='500400000400'):
        return 3
    elif(string=='500400000300'):
        return 4
    elif(string=='500400000200'):
        return 5
    elif(string=='500400000100'):
        return 6
    else :
        return 0
def get_is_school_district(string):
    if(string=='\N'):
        return 0
    else:
        try:
            return int(string)
        except Exception,e:
            return 0
    
def get_fitment_type_code(string):
    string=string.strip();
    if( string=='\N'):
        return 0
    elif(string=='112100000001'):
        return 1
    elif(string=='112100000002'):
        return 2
    elif(string=='112100000004'):
        return 3
    else :
        return 0
        
def get_total_floor(string):     
    if( string=='\N'):
        return 0
    elif(string.endswith('层')):
        try:
           return  int(string[0:-1])
        except Exception , e:
            return 0
    else :
        try:
            return int(string)
        except Exception ,e:
            return 0

def get_dealdate(string):
    if( string=='\N'):
        return 0
    try:
        curr=datetime.datetime.strptime(string,"%Y%m%d")
        curr_year=curr.year
        curr_month=curr.month
        
        origin=datetime.datetime.strptime(ORIGIN_DATE,"%Y%m%d")
        origin_year=origin.year
        origin_month=origin.month
        return (curr_year-origin_year)*12+curr_month-origin_month
       
    except:
        return 0
def get_money(string):
    string=string.strip()
    try:
        temp=float(string)
        if(temp<=10000):
            temp*=10000
        return temp
    except Exception,e:
        return 0
    



def floor_info(floor,total_floor):
    if(total_floor<=3):
        return floor
    elif(total_floor<8 and total_floor>=4):
        if(floor==1):
            return 2
        elif(floor==total_floor):
            return 4
        elif((floor>=2 and floor<=3 and total_floor<=6 )or (floor>=2 and floor<=4 and total_floor==7)):
            return 8
        elif((total_floor<=5 and floor==total_floor-1) or (total_floor>=6 and floor<total_floor and floor>=total_floor-2)):
            return 10
        else:
            return 0
    else:
        if(floor==1):
            return 1
        elif(floor==total_floor):
            return 2
        else:
            return int(round((floor*1.0/total_floor*1.0)*10))

if __name__=='__main__':
   
   print  datetime.datetime.today().year
   
  
    
    
    
    
    
    
    
     

  