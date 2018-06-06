###############################################################################
# Utility program distributed with the A.U.TH. Seismological Network dataless #
# SEED files.                                                                 #
#                                                                             #
# Usage: python plot_response.py station_code [datetime]                      #
#                                                                             #
# Plots the combined response of the vertical component of the seismometer    #
# and digitizer that were installed at a given station at a given date and    #
# time. The response information is expected to be found in the directory     #
# ../HTdataless_full_history in the file HT.sta.dataless, where sta is the    #
# station code.                                                               #
# If a date/time is not given, it is set to the present time. It is assumed   #
# that there is only one vertical channel per station at any time.            #
#                                                                             #
# It uses the ObsPy Python Toolbox (www.obspy.org)                            #
#                                                                             #
# 2017 Odysseus Galanis, A.U.Th. Seismological Network                        #
###############################################################################

import matplotlib.pyplot as plt
import dateutil.parser
import sys
from obspy import read_inventory, UTCDateTime

if (len(sys.argv) < 2 or len(sys.argv) > 3 ):
    sys.exit("Usage: python {:s} station_code [datetime]".format(sys.argv[0]))
sta=sys.argv[1]

if (len(sys.argv) > 2 ):
    try:
        t0 = dateutil.parser.parse(sys.argv[2])
    except:
        print "Datetime could not be parsed. Using current date and time"
        t0 = UTCDateTime.now()
else:
    t0 = UTCDateTime.now()

t0str=t0.isoformat()

try:
    inv=read_inventory("../HTdataless_full_history/HT.{:s}.dataless".format(sta),
                                                        format="SEED")
except:
    sys.exit("No response information found for station {:s}".format(sta))

inv=inv.select(channel="*Z",time=t0)

if not inv:
    sys.exit("No response information found for station {:s} on {:s}".format(
                                                                sta,t0str))

inv.plot_response(0.001, output='VEL',show=False)

net = inv.networks[0].code
loc = inv.networks[0].stations[0].channels[0].location_code
cha = inv.networks[0].stations[0].channels[0].code

fig = plt.gcf()
fig.suptitle("Response for {:s}.{:s}.{:s}.{:s} at {:s}".format(
                                                        net,sta,loc,cha,t0str),
             fontsize=12, fontweight='bold')

plt.show()

