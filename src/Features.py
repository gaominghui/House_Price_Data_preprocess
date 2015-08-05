# -*- coding: utf8 -*-

import sys
import os
from Get_Features_Method import *
from items_index import *
from biz_scale import *
#global MIN_BEDROOM
MIN_BEDROOM=sys.maxint
#global MAX_BEDROOM
MAX_BEDROOM=-1

#global MIN_PARLOR
MIN_PARLOR=sys.maxint
#global MAX_PARLOR
MAX_PARLOR=-1

#global MIN_TOILET
MIN_TOILET=sys.maxint
#global MAX_TOILET
MAX_TOILET=-1

#global MIN_COOKROOM
MIN_COOKROOM=sys.maxint
#global MAX_COOKROOM
MAX_COOKROOM=-1


#global MIN_BUILDSIZE
MIN_BUILDSIZE=sys.maxint
#global MAX_BUILDSIZE
MAX_BUILDSIZE=-1

#global MIN_FACE
MIN_FACE=sys.maxint
#global MAX_FACE
MAX_FACE=-1

#global MIN_YEAR
MIN_YEAR=sys.maxint
#global MAX_YEAR
MAX_YEAR=-1


#global MIN_DISTANCE_METRO_CODE
MIN_DISTANCE_METRO_CODE=sys.maxint
#global MAX_DISTANCE_METRO_CODE
MAX_DISTANCE_METRO_CODE=-1

#global MIN_FITMENT
MIN_FITMENT=sys.maxint
#global MAX_FITMENT
MAX_FITMENT=-1

#global MIN_FLOOR_SCALE
MIN_FLOOR_SCALE=sys.maxint
#global MAX_FLOOR_SCALE
MAX_FLOOR_SCALE=-1

#global MIN_DEALDATE
MIN_DEALDATE=sys.maxint
#global MAX_DEALDATE
MAX_DEALDATE=-1
month_dic={}
def pre_preprocess_read(data_file):
    global MIN_BEDROOM
    global MAX_BEDROOM
    global MIN_PARLOR
    global MAX_PARLOR
    global MIN_TOILET
    global MAX_TOILET
    global MIN_COOKROOM
    global MAX_COOKROOM
    global MIN_BUILDSIZE
    global MAX_BUILDSIZE
    global MIN_FACE
    global MAX_FACE
    global MIN_YEAR
    global MAX_YEAR
    global MIN_DISTANCE_METRO_CODE
    global MAX_DISTANCE_METRO_CODE
    global MIN_FITMENT
    global MAX_FITMENT
    global MIN_FLOOR_SCALE
    global MAX_FLOOR_SCALE
    global MIN_DEALDATE
    global MAX_DEALDATE
    
    features=[]
    fileHanler=open(data_file)
    
    for line in fileHanler.readlines():
        splits=line.strip().split('\t')
      
        bedroom_amount=get_bedroom_amout(splits[BEDROOM_AMOUNT_INDEX])
        if(bedroom_amount<MIN_BEDROOM):
            MIN_BEDROOM=bedroom_amount
        if(bedroom_amount>MAX_BEDROOM):
            MAX_BEDROOM=bedroom_amount
        parlor_amount=get_parlor_amout(splits[PARLOR_AMOUNT_INDEX])
        if(parlor_amount<MIN_PARLOR):
            MIN_PARLOR=parlor_amount
        if(parlor_amount>MAX_PARLOR):
            MAX_PARLOR=parlor_amount
        toilet_amount=get_toilet_amout(splits[TOILET_AMOUNT_INDEX])
        if(toilet_amount<MIN_TOILET):
            MIN_TOILET=toilet_amount
        if(toilet_amount>MAX_TOILET):
            MAX_TOILET=toilet_amount
        cookroom_amount=get_cookroom_amout(splits[COOKROOM_AMOUNT_INDEX])
        if(cookroom_amount<MIN_COOKROOM):
            MIN_COOKROOM=cookroom_amount
        if(cookroom_amount>MAX_COOKROOM):
            MAX_COOKROOM=cookroom_amount
        #room_detail=bedroom_amount*0.5+parlor_amount+toilet_amount*0.5+cookroom_amount*0.5
        floor=get_floor_name(splits[FLOOR_INDEX])
       
        build_size=get_build_size(splits[BUILD_SIZE_INDEX])
        if( build_size<1.0):
            print "build_size",build_size
            continue
        if(build_size<MIN_BUILDSIZE):
            MIN_BUILDSIZE=build_size
        if(build_size>MAX_BUILDSIZE):
            MAX_BUILDSIZE=build_size
        
        face=get_face_code(splits[FACE_NAME_INDEX])
        if(face<MIN_FACE):
            MIN_FACE=face
        if(face>MAX_FACE):
            MAX_FACE=face
        #print '{0}{1}'.format(splits[FACE_NAME_INDEX], str(face))
        year=get_build_end_year(splits[BUILD_END_YEAR_INDEX])
        if(year<MIN_YEAR):
            MIN_YEAR=year
        if(year>MAX_YEAR):
            MAX_YEAR=year
        
        #is_sales_tax=get_is_sales_tax(splits[IS_SALEX_TAX_INDEX])
        
        #property_fee=get_property_fee(splits[PROPERTY_FEE_INDEX])
        
        distance_metro_code=get_distance_metro_code(splits[DISTANCE_METRO_CODE_INDEX])
        if(distance_metro_code<MIN_DISTANCE_METRO_CODE):
            MIN_DISTANCE_METRO_CODE=distance_metro_code
        if(distance_metro_code>MAX_DISTANCE_METRO_CODE):
            MAX_DISTANCE_METRO_CODE=distance_metro_code
        #is_school_distinct=get_is_school_district(splits[IS_SCHOOL_DISTRICT_INDEX])
       
        fitment=get_fitment_type_code(splits[FITMENT_INDEX])
        is_school_district =get_is_school_district(splits[IS_SCHOOL_DISTRICT_INDEX]);
        
        if(fitment<MIN_FITMENT):
            MIN_FITMENT=fitment
        if(fitment>MAX_FITMENT):
            MAX_FITMENT=fitment
        
        total_floor=get_total_floor(splits[TOTAL_FLOOR_INDEX])
        if(floor>total_floor):
            #print floor,total_floor
            continue
        floor_scale=floor_info(floor, total_floor)
        #print floor,total_floor,floor_scale
        if(floor_scale<MIN_FLOOR_SCALE):
            MIN_FLOOR_SCALE=floor_scale
        if(floor_scale>MAX_FLOOR_SCALE):
            MAX_FLOOR_SCALE=floor_scale
        dealdate=get_dealdate(splits[DEAL_DATE_INDEX])
       
        if(dealdate<MIN_DEALDATE):
            MIN_DEALDATE=dealdate
        if(dealdate>MAX_DEALDATE):
            MAX_DEALDATE=dealdate
        
        money=get_money(splits[MONEY_INDEX])
        if month_dic.has_key(dealdate):
            arr=month_dic.get(dealdate)
            arr[0]+=money
            arr[1]+=build_size
            month_dic[dealdate]=arr
        else:
            arr=[]
            arr.append(money)
            arr.append(build_size)
            month_dic[dealdate]=arr
        feature=[bedroom_amount,parlor_amount,toilet_amount,cookroom_amount,\
                build_size,face,year,distance_metro_code,\
                fitment,floor_scale,dealdate,is_school_district,money]
        
        
        features.append(feature)
    return features

def pre_process_normalization(features,out_file):
    biz_scale=get_biz_scale("rongfeng2008_biz_mean_price.txt")
    for k,v in biz_scale.items():
        print k,v
    result_dic={}
    for (k,v) in month_dic.items():
        result_dic[k]=v[0]/v[1]
    month_mean_price_handler=open("month_mean_price.txt","w")
    month_mean_price_handler.write("month"+"\t"+"price"+"\n")
    for k,v in result_dic.items():
        month_mean_price_handler.write(str(k)+"\t"+str(v)+"\n")
    month_mean_price_handler.close()
    '''
    print MIN_BEDROOM
    print MAX_BEDROOM
    print MIN_PARLOR
    print MAX_PARLOR
    print MIN_TOILET
    print MAX_TOILET
    print MIN_COOKROOM
    print MAX_COOKROOM
    print MIN_BUILDSIZE
    print MAX_BUILDSIZE
    print MIN_FACE
    print MAX_FACE
    print MIN_YEAR
    print MAX_YEAR
    print MIN_DISTANCE_METRO_CODE
    print MAX_DISTANCE_METRO_CODE
    print MIN_FITMENT
    print MAX_FITMENT
    print MIN_FLOOR_SCALE
    print MAX_FLOOR_SCALE
    print MIN_DEALDATE
    print MAX_DEALDATE
    '''
    '''
    for feature in features:
        feature[0]=(feature[0]-MIN_BEDROOM)*1.0/(MAX_BEDROOM-MIN_BEDROOM)*1.0
        feature[1]=(feature[1]-MIN_PARLOR)*1.0/(MAX_PARLOR-MIN_PARLOR)*1.0
        feature[2]=(feature[2]-MIN_TOILET)*1.0/(MAX_TOILET-MIN_TOILET)*1.0
        feature[3]=(feature[3]-MIN_COOKROOM)*1.0/(MAX_COOKROOM-MIN_COOKROOM)*1.0
        feature[4]=(feature[4]-MIN_BUILDSIZE)*1.0/(MAX_BUILDSIZE-MIN_BUILDSIZE)*1.0
        feature[5]=(feature[5]-MIN_FACE)*1.0/(MAX_FACE-MIN_FACE)*1.0
        feature[6]=(feature[6]-MIN_YEAR)*1.0/(MAX_YEAR-MIN_YEAR)*1.0
        feature[7]=(feature[7]-MIN_DISTANCE_METRO_CODE)*1.0/(MAX_DISTANCE_METRO_CODE-MIN_DISTANCE_METRO_CODE)*1.0
        feature[8]=(feature[8]-MIN_FITMENT)*1.0/(MAX_FITMENT-MIN_FITMENT)*1.0
        feature[9]=(feature[9]-MIN_FLOOR_SCALE)*1.0/(MAX_FLOOR_SCALE-MIN_FLOOR_SCALE)*1.0
        feature[10]=(feature[10]-MIN_DEALDATE)*1.0/(MAX_DEALDATE-MIN_DEALDATE)*1.0
    '''
    file_out_handler=open(out_file,'w')
    file_out_handler.write("bedroom"+","+"parlor"+","+"toilet"+","+"cookroom"+","+"build_size"+","+"face"+","+\
                       "year"+","+\
                       "distance_metro_code"+","+"fitment"+","+\
                       "floor_total_floor_scale"+","+"dealdate"+","+"is_school_district"+","+"money"+","+"biz_scale"+"\n")
    '''
    for feature in features:
        for i in range(len(feature)):
            if i<len(feature)-1:
                file_out_handler.write(str(feature[i])+",")
            else:
                file_out_handler.write(str(feature[i]))
        file_out_handler.write("\n")
        file_out_handler.flush()
    file_out_handler.close()
    '''
    for feature in features:
        if(feature[10]<156):
            continue
        for i in range(len(feature)):
            file_out_handler.write(str(feature[i])+",")
        file_out_handler.write(str(biz_scale.get(feature[10])))   
        file_out_handler.write("\n")
        file_out_handler.flush()
    file_out_handler.close()
    
if __name__=='__main__':
    pre_process_normalization(pre_preprocess_read('rongfeng2008_chengjiao_2.txt'),'rongfeng2008_with_biz_scale.txt')
    print('done')

    
    
    


        
    
