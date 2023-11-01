import random
class station:
    def __init__(self, ctd_arr):
        self.arr = ctd_arr
        self.packets_sent = 0
        
        self.w0 = 8
        self.window = self.w0
        self.wMax = 512
        self.countdown = random.randint(0,self.window-1)
        self.queue = 0
        
    def findQ(self, time):
        i = 0
        while(i < len(self.arr) and self.arr[i] <= time):
            i += 1

        q =  i - self.packets_sent
        self.queue = q
        if(q < 0):
            return 0
        else:
            return q
    def find_next_frame(self, time):
        i = 0
        while(self.arr[i] < time):
            i += 1

        return self.arr[i]
    def get_new_ctdn(self):
        self.countdown = random.randint(0,self.window-1)
    def double_countdown(self):
        if self.window == self.wMax:
            self.get_new_ctdn()
            return
        else:
            self.window = self.window * 2
            self.get_new_ctdn()
    def renew_ctn(self):
        self.window = self.w0
        self.get_new_ctdn()
    

    


