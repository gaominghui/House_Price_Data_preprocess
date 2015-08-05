#encoding=utf8
'''

@author: gao
'''
ORIGIN_DATE='20000101'
import datetime
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
    
def get_biz_scale(file):
    file_handler=open(file);
    biz_scale={}
    biz_temp={}
    for line in file_handler :
        line=line.strip()
        splits=line.split()        
        biz_temp[get_dealdate(splits[5][0:8])]=float(splits[4])
    for k,v in biz_temp.items():
        biz_scale[k]=v/biz_temp[185]
    return biz_scale
    
        
if __name__=='__main__':
    get_biz_scale("rongfeng2008_biz_mean_price.txt")
        
    