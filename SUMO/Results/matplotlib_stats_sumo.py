import os, sys
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

base = os.path.dirname(__file__)
stats_path = os.path.join(base, "stats.xml")
if len(sys.argv) > 1:
    stats_path = sys.argv[1]
if not os.path.exists(stats_path):
    print("stats.xml not found:", stats_path); sys.exit(1)

tree = ET.parse(stats_path)
root = tree.getroot()

def get_attribs(tag):
    el = root.find(tag)
    return el.attrib if el is not None else {}

# Vehicles
veh = get_attribs("vehicles")
veh_keys = ["loaded", "inserted", "running", "waiting"]
veh_vals = [int(float(veh.get(k, 0))) for k in veh_keys]
plt.figure(figsize=(6,4))
plt.bar(veh_keys, veh_vals, color="tab:blue")
plt.title("Vehicles")
plt.ylabel("count")
f1 = os.path.join(base, "vehicles.png")
plt.savefig(f1, bbox_inches="tight")
plt.close()

# Teleports
tele = get_attribs("teleports")
tel_keys = ["total","jam","yield","wrongLane"]
tel_vals = [int(float(tele.get(k, 0))) for k in tel_keys]
plt.figure(figsize=(6,4))
plt.bar(tel_keys, tel_vals, color="tab:orange")
plt.title("Teleports")
plt.ylabel("count")
f2 = os.path.join(base, "teleports.png")
plt.savefig(f2, bbox_inches="tight")
plt.close()

# Vehicle trip statistics (numeric metrics)
vts = get_attribs("vehicleTripStatistics")
trip_keys = ["routeLength","speed","duration","waitingTime","timeLoss","departDelay"]
trip_vals = []
for k in trip_keys:
    val = vts.get(k)
    try:
        trip_vals.append(float(val) if val is not None else 0.0)
    except:
        trip_vals.append(0.0)
plt.figure(figsize=(8,4))
plt.bar(trip_keys, trip_vals, color="tab:green")
plt.title("Vehicle trip statistics (averages / totals)")
plt.xticks(rotation=25, ha="right")
f3 = os.path.join(base, "trip_stats.png")
plt.savefig(f3, bbox_inches="tight")
plt.close()

print("Saved:", f1, f2, f3) 