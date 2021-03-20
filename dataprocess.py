import re
class MPdataprocess:
    def __init__(self):
        self.data=[[]for i in range(7)]
        pass

    def liner_intert(self,t,t1,x1,t2,x2):
        return x1 + ((t-t1)/(t2-t1))*(x2-x1)


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
                    gyro = l_list
                elif l_list[0] == 'MAGN':
                    if magn == None:
                        alread_feature+=1
                    magn = l_list
                elif l_list[0] == 'PRES':
                    if pres == None:
                        alread_feature+=1
                    pres = l_list
                elif l_list[0] == 'AHRS':
                    if ahrs == None:
                        alread_feature+=1
                    ahrs = l_list
                if alread_feature == 5:
                    self.begin_time = l_list[2]

    def load(self,filedir):
        # acce gyro magn pres ahrs wifi gnss
    #data   0    1    2    3    4   5     6
    #以上为数据对应关系data 为7*n的矩阵
        with open(filedir) as file_object:
            for line in file_object:
                l_list = re.split(r'[;\s]', line.strip())
                #需要读入buffer的数据
                if l_list[0]!='%' and l_list[2]>=self.begin_time:
                    #不同类型传感器存放位置不同 对齐不同
                    if l_list[0] == 'ACCE':
                        self.data[0].append(l_list)
                    elif l_list[0] == 'GYRO':
                        self.data[1].append(l_list)
                    elif l_list[0] == 'MAGN':
                        self.data[2].append(l_list)
                    elif l_list[0] == 'PRES':
                        self.data[3].append(l_list)
                    elif l_list[0] == 'AHRS':
                        self.data[4].append(l_list)
                    elif l_list[0] == 'WIFI':
                        l = len(self.data[5])
                        ##去重
                        if (l>0 and self.data[5][l-1] != l_list) or l==0:
                                self.data[5].append(l_list)
                    elif l_list[0] == 'GNSS':
                        l = len(self.data[6])
                        if (l > 0 and self.data[6][l - 1] != l_list) or l == 0:
                            self.data[6].append(l_list)
        #对齐时间
        for i in range(len(self.data)):
            if i<5:
                d = self.data[i][0][2]-self.begin_time
                for i in self.data[i]:
                    i[2]=i[2]-d;
        self.end_time =
        #插值
        #需要的数据