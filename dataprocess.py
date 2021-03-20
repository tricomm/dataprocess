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
                if line == "":
                    continue
                l_list = re.split(r'[;\s]',line.strip())
                if len(l_list) < 3:
                    continue
                if l_list[0]=='%' and l_list[1] == 'WIFI' and l_list[2]=='data:':
                    if l_list[8] =='Frequency':
                        self.wifi_equ_frequency = True
                    else:
                        self.wifi_equ_frequency = False

                if l_list[0]=='%':
                    continue
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
                    self.begin_time = float(l_list[2])
                    return

    def load(self,filedir):
        self.perprocess(filedir)
        # acce gyro magn pres ahrs wifi gnss
    #data   0    1    2    3    4   5     6
    #以上为数据对应关系data 为7*n的矩阵
        with open(filedir) as file_object:
            for line in file_object:
                l_list = re.split(r'[;\s]', line.strip())
                #需要读入buffer的数据
                if l_list[0]=='%' or len(l_list)<3:
                    continue
                if l_list[0]!='%' and float(l_list[2])>=self.begin_time:

                    #将读入的数据都变成float 方便后续计算
                    for i in range(1,len(l_list)):
                        if l_list[0]=="WIFI" and i==6:
                            pass
                        else:
                            try:
                                l_list[i] = float(l_list[i])
                                break
                            except:
                                pass
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
                d = float(self.data[i][0][2])-self.begin_time
                for j in self.data[i]:
                    j[2]=float(j[2])-d
        self.end_time = min(self.data[0][-1][2],self.data[1][-1][2],self.data[2][-1][2],
                            self.data[3][-1][2],self.data[4][-1][2])

        #插值 采样周期必须为5ms的公倍数   k到k+1中间插值
        inter_data =[[]for i in range(7)]
        for i in range(5):
            # 未插值的data指针
            k = 0
            for j in range(int((self.end_time-self.begin_time)/0.005) +1):
                #直接写入
                if self.data[i][k][2] == self.begin_time+j*0.005:
                    k=k+1
                    inter_data[i].append(self.data[i][j])
                else:
                    inter_data[i].append([])
                    inter_data[i][-1].append(self.data[i][k][0])
                    inter_data[i][-1].append(self.data[i][k][1])
                    inter_data[i][-1].append(self.begin_time+j*0.005)
                    #对第l=3到n 个特征的线性插值
                    for l in range(3,len(self.data[i][k])):
                        inter_data[i][-1].append(self.liner_intert(self.begin_time+j*0.005,
                                                                   float(self.data[i][k][2]),
                                                                   float(self.data[i][k][l]),
                                                                   float(self.data[i][k+1][2]),
                                                                   float(self.data[i][k+1][l])))
        inter_data[5]=self.data[5]
        inter_data[6]=self.data[6]
        self.data = inter_data



    def imu_process(self):
        with open("imu.txt",'w') as file_write:
            for i in range(int((self.end_time-self.begin_time)/0.005) +1):
                line = str(self.begin_time+i*0.005)+","+str(self.data[0][i][3])+","+str(self.data[0][i][4])+","+str(self.data[0][i][5])\
                                                    +"," + str(self.data[1][i][3]) + "," + str(self.data[1][i][4]) + "," + str(self.data[1][i][5])\
                                                    +"," + str(self.data[2][i][3]) + "," + str(self.data[2][i][4]) + "," + str(self.data[2][i][5])\
                                                    +","+str(self.data[4][i][3])+","+str(self.data[4][i][4])+","+str(self.data[4][i][5])\
                                                    +","+str(self.data[3][i][3])+'\n'
                file_write.write(line)

    def wifi_process(self):
        with open("wifi.txt", 'w') as file_write:
            for i in range(len(self.data[5])):
                Ctime = str(float(self.data[5][i][2])-self.begin_time)
                c2=str(int(self.data[5][i][4].replace(":",""),16))
                c3=str(self.data[5][i][6]) if self.wifi_equ_frequency else str(self.data[5][i][5])
                line = Ctime+','+c2+','+c3+'\n'
                file_write.write(line)
    def gnss_process(self):
        with open("gnss.txt",'w') as file_write:
            begin_time = self.data[6][0][1]
            for i in range(len(self.data[6])):
                line = str(self.data[6][i][1]-begin_time)+','+str(self.data[6][i][2])\
                +',' + str(self.data[6][i][3])+','+str(self.data[6][i][4])+','+str(self.data[6][i][5])\
                +',' + str(self.data[6][i][6])+','+str(self.data[6][i][7])+','+str(self.data[6][i][9])\
                +',' + str(self.data[6][i][10])+'\n'
                file_write.write(line)


def main():
    dataprocess = MPdataprocess()
    dataprocess.load("EVALUATION(1).txt")
    #dataprocess.imu_process()
    dataprocess.wifi_process()
    #dataprocess.gnss_process()

if __name__ == '__main__':
    main()