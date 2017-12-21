###############################################################################
# Utility program distributed with the A.U.TH. Seismological Network dataless #
# SEED files.                                                                 #
#                                                                             #
# Usage: python network_history.py                                            #
#                                                                             #
# Displays a brief history of changes in all stations of the network. The     #
# information is expected to be found in the directory ../HTdataless in files #
# named *.dataless.                                                           #
# It is assumed that there is only one vertical channel per station at any    #
# time.                                                                       #
#                                                                             #
# It uses the ObsPy Python Toolbox (www.obspy.org)                            #
#                                                                             #
# 2017 Odysseus Galanis, A.U.Th. Seismological Network                        #
###############################################################################

from obspy import read_inventory, UTCDateTime
import sys
import string
import glob

if (len(sys.argv)) > 1:
    sys.exit("Usage: {:s}".format(sys.argv[0]))

inv_dir = glob.glob("../HTdataless/*.dataless")
if not inv_dir:
    sys.exit("No .dataless files found in the directory ../HTdataless")

print "\nNetwork history\n"
print ("{:^19.19s} {:^19.19s} {:3.3s} {:6.6s} {:40.40s} {:^10.10s} "
       "{:^11.11s} {:^6.6s} {:2.2s} {:>4.4s} {:50.50s}").format(
       "start", "end", "net", "sta", "description", "lat", "lon",
       "elev", "ch", "sps", "instrumentation")
print "-"*180

for f in inv_dir:

    inv=read_inventory(f,format="SEED")

    inv=inv.select(channel="*Z")

    for network in inv:
        for station in network:
             items = station.get_contents().items()
             for item in items:
                 if item[0]=="stations":
                     sta_long=item[1][0]
                     i0 = string.find(sta_long,"(") + 1
                     i1 = string.rfind(sta_long,")")
                     sta_long=sta_long[i0:i1]
             for channel in station:
                 net = network.code
                 sta = station.code
                 t0 = channel.start_date
                 if t0:
                     t0_str=t0.strftime("%Y-%m-%d %H:%M:%S")
                 else:
                     t0_str=""
                 t1 = channel.end_date
                 if t1:
                     t1_str=t1.strftime("%Y-%m-%d %H:%M:%S")
                 else:
                     t1_str=""
                 cha = channel.code
                 lat = channel.latitude
                 lon = channel.longitude
                 ele = channel.elevation
                 sps = channel.sample_rate
                 sns = channel.sensor.type
                 print ("{:19.19s} {:19.19s} {:3.3s} {:6.6s} {:40.40s} "
                        "{:10.5f} {:11.5f} {:6.1f} {:2.2s} {:4.0f} "
                        "{:50.50s}").format(
                        t0_str, t1_str, net, sta, sta_long, lat, lon, ele,
                        cha[0:2], sps, sns)

print "-"*180, "\n"

