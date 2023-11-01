import random 
import math
from node import station

#def find_next_frame(delivery_arr, time):

def check_for_idle(stat_arr, time):
    for station in stat_arr:
        if station.findQ(time) != 0:
            return False
    return True
def create_posson(lam_val, n):
    x = []
    sum = []
    for i in range(0,int(n*1.5)):
        u_temp = random.random()
        x_temp = (-1/lam_val) * math.log(1-u_temp)
        x.append(x_temp)
        if(i == 0):
            sum.append(x[i] * 100000)
        else:
            sum.append((x[i]*100000)+sum[i-1])
    int_sum = []
    for i in range(0, int(n*1.5)):
        int_sum.append(int(sum[i]))
    return int_sum







    
    
def find_next_frame(stat_arr, time):
    min_frame = 0
    
    station_A = stat_arr[0].find_next_frame(time)
    station_B = stat_arr[1].find_next_frame(time)

    if(station_A < station_B):
        return station_A
    else:
        return station_B
    
    

lam_val = 1000
number = lam_val * 10

slots_per_frame = 115
SIFS = 1
DIFS = 4
ACK = 3
RTS = 3
CTS = 3

station_A = station(create_posson(lam_val,number))
station_B = station(create_posson(lam_val,number))
station_arr = [station_A,station_B]
A_Collisions = 0
B_Collisions = 0

outcomes = [0,0,0,0,0,0,0,0,0,0,0,0,0]

time = 0
end = 1000000
A_last = DIFS
A_trans = 0
B_last = DIFS
B_trans = 0
next_invalid = False

while((A_last < end) and (B_last < end)):
    
    
        
    if(station_A.findQ(A_last) == 0):
        A_next = station_A.find_next_frame(A_last) + station_A.countdown
    else:
        A_next = A_last + station_A.countdown
    if(station_B.findQ(B_last) == 0):
        B_next = station_B.find_next_frame(B_last) + station_B.countdown
    else:
        B_next = B_last + station_B.countdown


    
    if(A_next < B_next):
        A_end = A_next + slots_per_frame
        A_trans += 1
        if(A_end > B_next or next_invalid):
            if(A_end > B_next):
                next_invalid = True
            else:
                next_invalid = False
            station_A.double_countdown()  
            A_last = A_end + SIFS + DIFS
            A_Collisions += 1          
        else:
            station_A.packets_sent += 1
            station_A.renew_ctn() 
            A_last = A_end + SIFS + DIFS + ACK   
            station_B.countdown += SIFS + DIFS +  ACK      

    else:

        B_end = B_next + slots_per_frame
        B_trans += 1
        if(B_end > A_next or next_invalid):
            if(B_end > A_next):
                next_invalid = True
            else:
                next_invalid = False
            station_B.double_countdown() 
            B_last = B_end + SIFS + DIFS  
            B_Collisions += 1         
        else:
            B_last = B_end + SIFS + DIFS + ACK
            station_B.packets_sent += 1
            station_B.renew_ctn()   
            station_A.countdown += SIFS + DIFS + ACK


            



    
        



        




    
    #print(A_last)
    #print(station_A.packets_sent)
    #print(station_B.packets_sent)
    
    

print(station_A.packets_sent)
print(A_Collisions)
print(station_B.packets_sent)
print(B_Collisions)
val = (A_Collisions + station_A.packets_sent)/(B_Collisions + station_B.packets_sent)            
print(val)