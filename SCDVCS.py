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
    
    

lam_val = 100
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
numCollisions = 0

outcomes = [0,0,0,0,0,0,0,0,0,0,0,0,0]

time = 0
end = 1000000

while(time < end):
    time += DIFS
    if check_for_idle(station_arr,time):
        # part where if there are no packets in the queue
        
        time = find_next_frame(station_arr,time)
        A_next = station_A.find_next_frame(time)
        B_next = station_B.find_next_frame(time)
        

        if(A_next + station_A.countdown < B_next + station_B.countdown):
            time = A_next + station_A.countdown
            if A_next + station_A.countdown > B_next:
                station_B.countdown -= A_next + station_A.countdown - B_next
            station_A.packets_sent += 1
            station_A.renew_ctn()
            outcomes[1] += 1
            #print("outcome1")

        if(B_next + station_B.countdown < A_next + station_A.countdown):
            time = B_next + station_B.countdown
            if B_next + station_B.countdown > A_next:
                station_A.countdown -= B_next + station_B.countdown - A_next
            station_B.packets_sent += 1
            station_B.renew_ctn()
            outcomes[2] += 1
            #print("outcome2")
        if(B_next + station_B.countdown == A_next + station_A.countdown):
            time = B_next + station_B.countdown
            station_A.double_countdown()
            station_B.double_countdown()
            numCollisions += 1
            outcomes[3] += 1
            #print("outcome3")
            time += RTS +  SIFS
            continue
            
        



    else:
        # someone is in the queue already
        if station_A.findQ(time) != 0:
            if station_B.findQ(time) != 0:
                if(station_A.countdown == station_B.countdown):
                    station_A.double_countdown()
                    station_B.double_countdown()
                    numCollisions += 1
                    outcomes[4] += 1
                    #print("outcome4")
                    time += RTS +  SIFS
                    continue

                else:
                    if(station_A.countdown < station_B.countdown):
                        station_B.countdown -= station_A.countdown
                        station_A.packets_sent += 1
                        station_A.renew_ctn()
                        outcomes[5] += 1
                        #print("outcom5")
                        
                    else:
                        station_A.countdown -= station_B.countdown
                        station_B.packets_sent += 1
                        station_B.renew_ctn()
                        outcomes[6] += 1
                        #print("outcome6")
            else:
                if time + station_A.countdown < station_B.find_next_frame(time) + station_B.countdown:
                    if time + station_A.countdown > station_B.find_next_frame(time):
                        station_B.countdown -= time + station_A.countdown - station_B.find_next_frame(time)
                    time = time + station_A.countdown
                    station_A.packets_sent += 1
                    station_A.renew_ctn()
                    outcomes[7] += 1
                    #print("outcome7")
                elif time + station_A.countdown > station_B.find_next_frame(time) + station_B.countdown:
                    
                    if time + station_B.countdown > station_A.find_next_frame(time):
                        station_A.countdown -= time + station_B.countdown - station_A.find_next_frame(time)
                    time = time + station_B.countdown
                    station_B.packets_sent += 1
                    #print("outcome8")
                    station_B.renew_ctn()
                    outcomes[8] += 1
                else:
                    time = time + station_A.countdown
                    station_A.double_countdown()
                    station_B.double_countdown()
                    numCollisions += 1
                    outcomes[9] += 1
                    #print("outcome9")
                    time += RTS +  SIFS
                    continue

        else:
            if time + station_B.countdown < station_A.find_next_frame(time) + station_A.countdown:
                if time + station_B.countdown > station_A.find_next_frame(time):
                    station_A.countdown -= time + station_B.countdown - station_A.find_next_frame(time)
                time = time + station_B.countdown
                station_B.packets_sent += 1
                station_B.renew_ctn()
                #print("outcome10")
                outcomes[10] += 1
            elif time + station_B.countdown > station_A.find_next_frame(time) + station_A.countdown:
                
                station_B.countdown -= time + station_B.countdown - station_A.find_next_frame(time) - station_A.countdown
                time = station_A.find_next_frame(time) + station_A.countdown
                station_A.packets_sent += 1
                station_A.renew_ctn()
                outcomes[11] += 1
                #print("outcome11")
            else:
                time = time + station_A.countdown
                station_A.double_countdown()
                station_B.double_countdown()
                numCollisions += 1
                outcomes[12] += 1
                #print("utcome12")
                time += RTS +  SIFS
                continue
    
    time += slots_per_frame + RTS + (2*SIFS) + CTS
    
    

print(station_A.packets_sent)
print(numCollisions)
print(station_B.packets_sent)
print(numCollisions)
val = (station_A.packets_sent + numCollisions)/(station_B.packets_sent + numCollisions)
print(val)
                











    







    
