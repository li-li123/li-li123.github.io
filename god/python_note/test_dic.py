import datetime

class SAL():
    def __sub__(self):       
        am_standard_time = datetime.time(8,30)
        am_working_time = datetime.time(9,30)
        pass


class MyTime:


    __time__ = datetime.time(8, 30)

    def get_houer(self):
        return self.__time__.hour

    def get_minute(self):
        return self.__time__.minute

    """
    获取当前时间距离 0 点过了多少分钟
    """
    def get_total_minute(self):
        return self.get_houer() * 60 + self.get_minute()

    def __init__(self, time:datetime.time):
         self.__time__ = time

    def __sub__(self, other):
        diff_minute = self.get_total_minute() - other.get_total_minute()
        time = datetime.time(diff_minute //60, diff_minute % 60)
        return MyTime(time)


    def __getitem__(self, index):
        return 0

if __name__ == '__main__':
    # start = datetime(hour = 12,minute = 30)
    # work_time = SAL()
    # print(work_time.morning())
    # print(datetime.datetime.now())

   start = MyTime(datetime.time(8, 30))
   print(start[88])
#    start = MyTime.__init__( datetime.time(8, 30))
   end = MyTime(datetime.time(12, 30))
   time_diff = end - start
#    time_diff = end.__sub__(start)
   print(time_diff.get_total_minute())