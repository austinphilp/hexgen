from hexgen import generate
from hexgen.enums import MapType

options = {
    "map_type": MapType.terran,
    "surface_pressure": 1013.25,
    "axial_tilt": 23,
    "size": 100,
    "base_temp": -19.50,
    "avg_temp": 12,
    "sea_percent": 50,
    "hydrosphere": True,
    "num_rivers": 125,
    "num_territories": 20,
}

gen = generate(options, image=True)
gen.export("output/world-data.json", pretty_copy=True)
