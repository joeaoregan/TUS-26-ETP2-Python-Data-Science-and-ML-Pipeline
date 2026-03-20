# SUMO Traffic Simulation — Athlone Network

A traffic simulation of a local road network built using [Eclipse SUMO](https://sumo.dlr.de/) v1.26.0. The simulation runs 7 predefined routes through the town network for a 12-hour period using real-world OSM map data.

---

## Requirements

- [Eclipse SUMO](https://sumo.dlr.de/docs/Downloads.php) v1.26.0 or later
- Python 3.x
- `SUMO_HOME` environment variable set (e.g. `C:\Program Files (x86)\Eclipse\Sumo`)
- Python packages: `pandas`, `beautifulsoup4` (only needed for data extraction scripts)

---

## Running the Simulation

```bat
run.bat
```

This launches `sumo-gui` with the main configuration file `osm.sumocfg`.

---

## How the Simulation Works

The active route configuration in `osm.sumocfg` is:

```xml
<route-files value="tii_flows.xml,town_routes.rou.xml"/>
```

- `town_routes.rou.xml` is the single active source of traffic. It defines 7 fixed routes with time-varying hourly flows derived from TII counts. Each route contains 12 hourly flow slots covering 07:00–19:00.
- Route split (new):
	- West entry (Bali side) is split across 3 routes:
		- bali-bali-goldenIsland
		- bali-bali-long
		- bali-shannon-short
	- East entry (B&Q side) is split across 4 routes:
		- bAndQ-shannon-orenge
		- bAndQ-bAndq-orenge
		- bAndQ-bAndQ-long
		- bAndQ-shannon-long
- `tii_flows.xml` is loaded but currently contains only a vehicle type definition and contributes no vehicles. All traffic originates from `town_routes.rou.xml`.

---

## Core Files (required to run the simulation)

| File | Purpose |
|------|---------|
| `osm.net.xml.gz` | The road network generated from OpenStreetMap data. The main network file used by SUMO. |
| `osm.sumocfg` | The main SUMO simulation configuration. Defines input files, simulation time (0–43200 s), output files, routing and TLS settings. |
| `town_routes.rou.xml` | Defines the 7 predefined routes with hourly time-varying flows derived from TII traffic counts. West counts are distributed across the 3 Bali routes; East counts are distributed across the 4 B&Q routes. 12 flow slots per route (one per hour, 07:00–19:00). |
| `tii_flows.xml` | Currently a placeholder. Contains only a `car` vehicle type definition. No flows are active. Loaded by SUMO but contributes vehicles to the simulation. |
| `tii_hourly_traffic.csv` | Source of the hourly East/West vehicle counts used to generate the flow rates in `town_routes.rou.xml`. Not read directly by SUMO — data was used to populate the flow values. |
| `osm.view.xml` | GUI display settings for `sumo-gui`. Sets the visual scheme to "real world" and a 20 ms simulation delay. |
| `run.bat` | One-click launcher. Runs `sumo-gui -c osm.sumocfg`. |

---

## Source & Reference Data

| File | Purpose |
|------|---------|
| `osm_bbox.osm.xml.gz` | Raw OpenStreetMap export for the bounding box area. Source input used by `netconvert` to build `osm.net.xml.gz`. |
| `osm.netccfg` | `netconvert` configuration used to convert the OSM data into the SUMO network. Enables left-hand traffic, actuated traffic lights, and street name output. |

---

## Simulation Output Files (generated on run)

| File | Purpose |
|------|---------|
| `edgeData.xml` | Per-edge traffic statistics (volume, speed, occupancy) collected every hour during simulation. |
| `tripinfos.xml` | Per-vehicle trip statistics (departure time, arrival time, duration, route length). |
| `stats.xml` | Overall simulation statistics summary. |

---
