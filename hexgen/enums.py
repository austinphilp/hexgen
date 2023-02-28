from enum import Enum

from hexgen.constants import TERRAIN_BARREN, TERRAIN_OCEANIC, TERRAIN_TERRAN


class SuperEnum(Enum):
    """Adds an id property that gets the order of an enum member in the class"""

    def __init__(self, *args):
        for key, value in enumerate(args):
            # TODO - replace __keys__ attr access
            for namekey, name in enumerate(self.__keys__):
                if key == namekey:
                    setattr(self, name, value)

    def to_dict(self):
        """converts an enum member to a dict"""
        rep = dict([(key, getattr(self, key)) for key in self.__keys__])
        rep["name"] = self.name
        return rep

    @classmethod
    def get(cls, id_):
        matching_items = [item for item in list(cls.__members__) if getattr(cls[item], "id") == id_]
        if len(matching_items) > 0:
            return cls[matching_items[0]]
        else:
            return None

    @classmethod
    def items(cls):
        return list(cls.__members__)

    @classmethod
    def pluck(cls, key="name"):
        return [getattr(cls[x], key) for x in list(cls.__members__)]

    @classmethod
    def dump(cls):
        return [cls[x].to_dict() for x in list(cls.__members__)]

    @classmethod
    def all(cls):
        return [cls[x].to_dict() for x in list(cls.__members__)]

    @classmethod
    def members(cls):
        return [cls[x].name for x in list(cls.__members__)]

    @classmethod
    def list(cls):
        return [cls[x] for x in list(cls.__members__)]


# https://jsfiddle.net/ajfu7em8/1/
class Biome(SuperEnum):
    __keys__ = ["id", "code", "title", "color", "base_fertility", "color_satellite"]

    lifeless = (13, "l", "Lifeless", (200, 200, 200), 0, (150, 150, 150))

    # terran
    arctic = (1, "a", "Arctic", (224, 224, 224), 1, (132, 152, 159))
    tundra = (2, "u", "Tundra", (114, 153, 128), 15, (52, 55, 44))
    alpine_tundra = (3, "p", "Alpine Tundra", (97, 130, 106), 10, (59, 60, 42))
    desert = (4, "d", "Desert", (237, 217, 135), 5, (94, 78, 52))
    shrubland = (5, "s", "Shrubland", (194, 210, 136), 20, (58, 47, 21))
    savanna = (6, "S", "Savanna", (219, 230, 158), 80, (66, 53, 28))
    grasslands = (7, "g", "Grasslands", (166, 223, 106), 150, (45, 46, 22))
    boreal_forest = (8, "b", "Boreal Forest", (28, 94, 74), 30, (36, 41, 29))
    temperate_forest = (9, "t", "Temperate Forest", (76, 192, 0), 100, (40, 37, 19))
    temperate_rainforest = (10, "T", "Temperate Rainforest", (89, 129, 89), 100, (42, 38, 21))
    tropical_forest = (11, "r", "Tropical Forest", (96, 122, 34), 70, (32, 39, 21))
    tropical_rainforest = (12, "R", "Tropical Rainforest", (0, 70, 0), 60, (26, 33, 16))

    # BARREN
    # color: grey if no atmosphere ( less than 0.003 earth pressure),
    #   red if atmosphere (greater than 0.003 earth pressure),
    #   tan if atmosphere and water
    # - highlands   light
    # - lowlands    dark
    barren_dusty = (14, "bld", "Barren Drylands", (87, 26, 27), 0)

    barren = (16, "bld", "Barren Drylands", (43, 44, 35), 0)
    barren_wet = (21, "bw", "Barren Wetland", (77, 36, 37), 0, (22, 51, 61))

    barren_ice_caps = (18, "bi", "Barren Ice Caps", (242, 228, 216), 0)

    # VOLCANIC
    # color: greyish light brown with red lava flows
    # - lava plains     red
    # - highlands       ligh
    # - lowlands        dark
    volcanic_liquid = (19, "mo", "Lava Fields", (217, 0, 0), 0)
    volcanic_molten_river = (19, "mo", "Lavaflow", (207, 10, 10), 0, (207, 10, 10))
    volcanic_solid = (20, "so", "Basaltic Plains", (40, 28, 25), 0)

    # ocean biomes?
    # estuary
    # coral reef
    # deep ocean
    # inland sea
    # mediterranean
    # arctic_ocean


class OceanType(SuperEnum):
    __keys__ = ["id", "title"]

    water = (1, "Water")
    magma = (2, "Magma")
    hydrocarbons = (3, "Hydrocarbons")


class HexResourceRating(SuperEnum):
    """((1 + 1) * 60/1000 ) / (60 ^ 2) * 10000"""

    __keys__ = ["id", "title", "rarity", "multiplier"]

    poor = (1, "Poor", 10, 4)
    average = (2, "Average", 6, 3)
    rich = (3, "Rich", 3, 2)
    abundant = (4, "Abundant", 1, 1)


class HexResourceType(SuperEnum):
    __keys__ = ["id", "rarity", "title", "material", "yield", "color"]

    iron_vein = (1, 100, "Iron Vein", 1000, "commonmetals", (100, 0, 0))
    copper_vein = (2, 80, "Copper Vein", 1000, "commonmetals", (0, 100, 0))
    lead_vein = (4, 60, "Lead Vein", 1000, "commonmetals", (100, 0, 100))
    zinc_vein = (6, 20, "Zinc Vein", 1000, "commonmetals", (150, 50, 50))
    tin_vein = (6, 20, "Tin Vein", 1000, "commonmetals", (150, 50, 50))

    silver_vein = (3, 20, "Silver Vein", 1000, "preciousmetals", (0, 0, 100))
    gold_ore_deposit = (7, 10, "Gold Ore Deposit", 500, "preciousmetals", (255, 0, 0))
    adamantine_ore_deposit = (3, 10, "Adamantine Ore Deposit", 500, "preciousmetals", (55, 89, 68))
    mithril_ore_deposit = (1, 10, "Mithril Ore Deposit", 500, "preciousmetals", (52, 140, 235))
    coal_deposit = (15, 20, "Coal Deposit", 1500, "carbon", (255, 255, 255))


class HexEdge(SuperEnum):
    __keys__ = ["id", "title", "short", "arrow"]
    east = (1, "East", "E", "→")
    north_east = (2, "North East", "NE", "↗")
    north_west = (3, "North West", "NW", "↖")
    west = (4, "West", "W", "←")
    south_west = (5, "South West", "SW", "↙")
    south_east = (6, "South East", "SE", "↘")


class MapType(SuperEnum):
    __keys__ = ["id", "title", "colors"]

    terran = (1, "Terran", TERRAIN_TERRAN)
    barren = (2, "Barren", TERRAIN_BARREN)
    gas = (3, "Gas", None)
    volcanic = (4, "Volcanic", TERRAIN_BARREN)
    oceanic = (5, "Oceanic", TERRAIN_OCEANIC)
    glacial = (6, "Barren", TERRAIN_BARREN)


class HexType(Enum):
    land = "Land"  # hex over or at sealevel
    ocean = "Ocean"  # hex under sealevel


class HexSurface(SuperEnum):
    """needed for temperature calculations"""

    __keys__ = ["id", "specific_heat", "albedo"]
    water_fresh = (1, 1.00, 0.0)  # water without salt
    water_sea = (2, 0.94, 0.0)  # water with salt
    granite = (3, 0.19, 0.0)  # continental crust in volcanically active planets
    basalt = (4, 0.20, 0.0)  # volcanic basaltic rock
    soil_wet = (5, 0.35, 0.0)  # soil with organic materials
    soil_dry = (6, 0.19, 0.0)  # desert soil
    soil_barren = (7, 0.10, 0.0)  # barren soil
    ice_warm = (8, 0.50, 0.0)  # ice warmer than -10 degrees F
    ice_cold = (9, 0.40, 0.0)  # ice warmer than -100 deg F to -10 deg F


class HexFeature(Enum):
    """Each hex can have multiple HexFeatures"""

    lake = "Lake"  # The terminus to a river if it didn't reach sealevel
    glacier = "Glacier"  # A water hex with a very low surface temperature

    # randomly placed
    volcano = "Volcano"  # Volcano: 1 hex or 2-ring or 3-ring
    lava_flow = "Lava Flow"
    crater = "Crater"  # depression of size 2-ring or 3-ring

    # bodies of water
    sea = "Sea"
    ocean = "Ocean"


class GeoformType(SuperEnum):
    """A grouping of like geographic features"""

    __keys__ = ["id", "title", "color"]

    # water
    ocean = (1, "Ocean", (0, 0, 255))  # > 100 water hexes
    sea = (2, "Sea", (50, 50, 200))  # < 100 water hexes
    strait = (3, "Strait", (100, 100, 150))  # a water hex with land on opposite sides and water in between them
    lake = (4, "Lake", (0, 0, 100))  # a group of up to 3 water hexes
    bay = (10, "Bay", (50, 50, 150))

    # land
    isthmus = (5, "Isthmus", (100, 150, 100))  # a land hex with water on opposite sides and land in between them
    small_island = (6, "Small Island", (200, 255, 200))  # < 25 land hexes
    large_island = (7, "Large Island", (100, 255, 100))  # < 100 land hexes
    continent = (8, "Continent", (0, 255, 0))  # > 100 land hexes
    peninsula = (9, "Peninsula", (0, 200, 0))  # group of land separated by an isthmus


class EdgeDirection(Enum):
    north = "North"
    south = "South"
    north_west = "North West"
    north_east = "North East"
    south_west = "South West"
    south_east = "South East"


class HexSide(Enum):
    east = "East"
    west = "West"
    north_west = "North West"
    north_east = "North East"
    south_west = "South West"
    south_east = "South East"

    def branching(self, direction):
        """Returns the hex sides that fork from this edge direction"""
        if self is HexSide.east or self is HexSide.west:
            if direction is EdgeDirection.north:
                return HexSide.south_west, HexSide.south_east
            else:  # elif direction is EdgeDirection.south:
                return HexSide.north_west, HexSide.north_east
        elif self is HexSide.south_east:
            if direction is EdgeDirection.north_east:
                return HexSide.west, HexSide.south_west
            else:  # elif direction is EdgeDirection.south_west:
                return HexSide.east, HexSide.north_east
        elif self is HexSide.south_west:
            if direction is EdgeDirection.north_west:
                return HexSide.east, HexSide.south_east
            else:  # elif direction is EdgeDirection.south_east:
                return HexSide.west, HexSide.north_west
        elif self is HexSide.north_west:
            if direction is EdgeDirection.south_west:
                return HexSide.east, HexSide.north_east
            else:  # elif direction is EdgeDirection.north_east:
                return HexSide.west, HexSide.south_west
        elif self is HexSide.north_east:
            if direction is EdgeDirection.north_west:
                return HexSide.east, HexSide.south_east
            else:  # elif direction is EdgeDirection.south_east:
                return HexSide.north_west, HexSide.west
        raise Exception("Branching invalid, Side: {}, Direction: {}".format(self, direction))


class Zones(SuperEnum):
    __keys__ = ["id", "title", "color", "map_key", "incr"]

    arctic_circle = (1, "Artic Circle", (150, 150, 250), "N", 0.60)
    northern_temperate = (2, "Northern Temperate", (150, 250, 150), "A", 0.90)
    northern_subtropics = (3, "Nothern Subtropics", (150, 250, 200), "B", 0.60)
    northern_tropics = (4, "Northern Tropics", (230, 150, 150), "C", 0.30)
    southern_tropics = (5, "Southern Tropics", (250, 180, 150), "D", 0.30)
    southern_subtropics = (6, "Southern Subtropics", (150, 250, 200), "E", 0.60)
    southern_temperate = (7, "Southern Temperate", (150, 250, 150), "F", 0.90)
    antarctic_circle = (8, "Antarctic Circle", (150, 150, 250), "S", 0.60)


class Hemisphere(Enum):
    northern = "Northern"
    southern = "Southern"


class Season(Enum):
    winter = "Winter"
    spring = "Spring"
    summer = "Summer"
    autumn = "Autumn"
