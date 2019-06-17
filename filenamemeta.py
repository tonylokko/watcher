import re
import os
import datetime
from pathlib import Path

string_example = "C1AF_00046_20190529082625.pcap"
hrsstring_example = "C1AF_2019_05_29_08_26_25_12345678.pcap"
pathexample = "/what/is/this/path/C1AF_00046_20190529082625.pcap"


'''
Lots of extra metadata to be added which we can get from the filename, e.g. C1AF_00046_20190529082625.pcap (recorderstap_pcapsequence_yearmonthdayhourminutesecond)
Recorder stamp
x-commandsystem-meta = can be “C” or “L”
x-highway-meta = can be “1” or “2”
x-cshcontroller-meta = can be either “A” or “F”
x-datafiltering-meta = can be either “f” or “u”
Pcap sequence number
x-pcapsequence-meta = 5 digit wireshark ID
Absolute timestamp
x-recordertimestamp-meta = yearmonthdayhourminutesecond
E.g. HRS file = C1AF_year_month_day_hour_minute_seconds_8digitappUUID
Recorder stamp
x-commandsystem-meta = can be “C” or “L”
x-highway-meta = can be “1” or “2”
x-cshcontroller-meta = can be either “A” or “F”
x-datafiltering-meta = can be either “f” or “u”
Time and Date
x-timeanddate-meta = year_month_day_hour_minute_seconds
'''



def pcapinterpret2(itemname):
    if len(itemname) <= 31:
        xcommandsystemmeta = itemname[0]
        xhighwaymeta = itemname[1]
        xcshcontrollermeta = itemname[2]
        xdatafilteringmeta = itemname[3]
        xpcapsequencemeta = itemname[5:10]
        xdatatimefromfile = datetime.datetime.strptime(itemname[11:25], '%Y%m%d%H%M%S').isoformat()
        metas.clear()
        metas.update({'x-command-system-meta': xcommandsystemmeta})
        metas.update({'x-highway-system-meta': xhighwaymeta})
        metas.update({'x-cshcontroller-meta': xcshcontrollermeta})
        metas.update({'x-data-filtering-meta': xdatafilteringmeta})
        metas.update({'x-datetimefromfile-meta': xdatatimefromfile})
        return metas
    else:
        xcommandsystemmeta = itemname[0]
        xhighwaymeta = itemname[1]
        xcshcontrollermeta = itemname[2]
        xdatafilteringmeta = itemname[3]
        xtimeanddatemeta = itemname[5:24]
        xappidmeta = itemname[25:33]
        metas.clear()
        metas.update({'x-command-system-meta': xcommandsystemmeta})
        metas.update({'x-highway-system-meta': xhighwaymeta})
        metas.update({'x-cshcontroller-meta': xcshcontrollermeta})
        metas.update({'x-data-filtering-meta': xdatafilteringmeta})
        metas.update({'x-timeanddate-meta': xtimeanddatemeta})
        metas.update({'x-appid-meta': xappidmeta})
        return metas

metas = {}
pcapinterpret2(string_example)
print(metas)

pcapinterpret2(hrsstring_example)
print(metas)

