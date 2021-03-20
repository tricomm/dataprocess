import re
class MPdataprocess:
    def __init__(self):
        pass

    def perprocess(self,filedir):
        alread_feature=0
        acce,gyro,magn,pres,ahrs = None,None,None,None,None
        acce_time,gyro_time,magn_tyme,pres_time,ahrs_time = None,None,None,None,None
        with open(filedir) as file_object:
            for line in file_object:
                '''逐行读取文件的每一行内容'''
                l_list = re.split(r'[;\s]',line.strip())
                if l_list[1] == 'WIFI' and l_list[2]=='data:':
                    if l_list[8] =='Frequency':
                        self.wifi_equ_frequency = True
                    else:
                        self.wifi_equ_frequency = False
                if l_list[0] =='ACCE':
                    if acce == None:
                        alread_feature+=1
                    acce = l_list
                elif l_list[0]=='GYRO':
                    if gyro == None:
                        alread_feature+=1
                    acce = l_list
                elif l_list[0] == 'MAGN':
                    if acce == None:
                        alread_feature+=1
                    acce = l_list
                elif l_list[0] == 'PRES':
                    if acce == None:
                        alread_feature+=1
                    acce = l_list
                elif l_list[0] == 'AHRS':
                    if acce == None:
                        alread_feature+=1
                    acce = l_list