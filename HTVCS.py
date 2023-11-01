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
A_trans = 0
B_trans = 0

outcomes = [0,0,0,0,0,0,0,0,0,0,0,0,0]

time = 0
end = 1000000
A_last = DIFS
B_last = DIFS
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
        
        A_end = A_next + RTS + SIFS
        
        if(A_end > B_next or next_invalid):#collision
            if(A_end > B_next):
                next_invalid = True
            else:
                next_invalid = False
           
            station_A.double_countdown()
            A_Collisions += 1
            A_last = A_end + SIFS + DIFS
            #print("1")
            outcomes[1] += 1
        elif(A_end == B_next):#rare situation
            A_next = A_end + CTS + SIFS + slots_per_frame
            station_A.double_countdown()
            A_Collisions += 1
            A_trans += 1
            while(B_next < A_next):
                station_B.double_countdown()
                B_Collisions += 1
                B_next += station_B.countdown + DIFS + RTS + SIFS
            #print("2")
            outcomes[2] += 1

        else:# successful packet transmission
            station_A.packets_sent += 1
            station_A.renew_ctn() 
            A_trans += 1
            if (B_next > A_end) and (B_next - station_B.countdown < A_end):
                station_B.countdown =  B_next - A_end
            A_last = A_end + SIFS + slots_per_frame + SIFS + ACK + DIFS
            B_last = A_last  
            #print("3") 
            outcomes[3] += 1        

    elif(B_next < A_next):
        B_end = B_next + RTS + SIFS
        
        if(B_end > A_next or next_invalid):#collision
            if(B_end > A_next):
                next_invalid = True
            else:
                next_invalid = False
           
            station_B.double_countdown() 
            B_Collisions += 1 
            B_last = B_end + SIFS + DIFS
            #print("4")
            outcomes[4] += 1
        elif(B_end == A_next):#rare situation
            B_next = B_end + CTS + SIFS + slots_per_frame
            station_B.double_countdown()
            B_Collisions += 1
            B_trans += 1
            while(A_next < B_next):
                station_A.double_countdown()
                A_Collisions += 1
                A_next += station_A.countdown + DIFS + RTS + SIFS
            #print("5")
            outcomes[5] += 1

        else:# successful packet transmission
            station_B.packets_sent += 1
            station_B.renew_ctn() 
            B_trans += 1
            if (A_next > B_end) and (A_next - station_A.countdown < B_end):
                station_A.countdown = A_next - B_end
            B_last = B_end + SIFS + slots_per_frame + SIFS + ACK + DIFS
            A_last = B_last
            #print("6")
            outcomes[6] += 1
    else:
        A_last = A_next + RTS + SIFS + CTS
        B_last = A_last
        station_A.double_countdown()
        station_B.double_countdown()
        A_Collisions += 1
        B_Collisions +=1
        #print("7")
        outcomes[7] += 1
    
    if(station_B.countdown > 512 or station_A.countdown > 512):
        print("oof")

    
print(station_A.packets_sent)
print(A_Collisions)
print(station_B.packets_sent)
print(B_Collisions)
val = (A_trans)/(B_trans)            
print(val)    



                