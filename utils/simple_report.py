###############################################################################
# Utility program distributed with the A.U.TH. Seismological Network dataless #
# SEED files.                                                                 #
#                                                                             #
# Usage: python simple_report.py [datetime]                                   #
#                                                                             #
# Displays a simple report of the state of the network at a given date and    #
# time. The response information is expected to be found in the directory     #
# ../HTdataless_AUTh in files named *.dataless.                               #
# If a date/time is not given, it is set to the present time. It is assumed   #
# that there is only one vertical channel per station at any time.            #
#                                                                             #
# It uses the ObsPy Python Toolbox (www.obspy.org)                            #
#                                                                             #
# 2017 Odysseus Galanis, A.U.Th. Seismological Network                        #
###############################################################################

from obspy import read_inventory, UTCDateTime
import sys
#import string
import dateutil.parser
import glob

if (len(sys.argv)) > 2:
    sys.exit("Usage: {:s} [datetime]".format(sys.argv[0]))
if (len(sys.argv)) > 1:
    try: 
        datetime = dateutil.parser.parse(sys.argv[1])
    except:
        print("Datetime could not be parsed. Using current date and time")
        datetime = UTCDateTime.now()
else:
    datetime = UTCDateTime.now()

inv_dir = glob.glob("../HTdataless_AUTh/*.dataless")
if not inv_dir:
    sys.exit("No .dataless files found in the directory " +
             "../HTdataless_AUTh")

datetime_str = datetime.isoformat()

print("\nState of the inventory at {:s} UTC\n".format(datetime_str))
print(('{:3.3s} {:6.6s} {:40.40s} {:^10.10s} {:^11.11s} {:^6.6s} '
       '{:2.2s} {:>4.4s} {:50.50s}').format(
       "net", "sta", "description", "lat", "lon",
       "elev", "ch", "sps", "instrumentation"))
print("-"*140)


for f in inv_dir:

    inv=read_inventory(f,format="SEED")

    inv=inv.select(channel="*Z",time=datetime)

    for network in inv:
        for station in network:
             items = station.get_contents().items()
             for item in items:
                 if item[0]=="stations":
                     sta_long=item[1][0]
#                     i0 = string.find(sta_long,"(") + 1
                     i0 = sta_long.find("(")
#                     i1 = string.rfind(sta_long,")")
                     i1 = sta_long.rfind(")")
                     sta_long=sta_long[i0:i1]
             for channel in station:
                 net = network.code
                 sta = station.code
                 cha = channel.code
                 lat = channel.latitude
                 lon = channel.longitude
                 ele = channel.elevation
                 sps = channel.sample_rate
                 sns = channel.sensor.type
                 print(("{:3.3s} {:6.6s} {:40.40s} {:10.5f} {:11.5f} "
                        "{:6.1f} {:2.2s} {:4.0f} {:50.50s}").format(
                        net, sta, sta_long, lat, lon, ele,
                        cha[0:2], sps, sns))

print("-"*140, "\n")

