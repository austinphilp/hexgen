from hexgen.draw import HexGridDraw
from hexgen.enums import GeoformType
from hexgen.hex import HexFeature
from hexgen.mapgen import MapGen


def draw_grid(hex_grid):
    def color_heightmap(h):
        alt = int(h.altitude)
        return (alt, alt, alt)

    def color_terrain(h):
        return h.color_terrain

    def color_rivers(h):
        return h.color_rivers

    def color_temperature_end_year(h):
        return h.color_temperature[0]

    def color_temperature_mid_year(h):
        return h.color_temperature[1]

    def temperature_end_year(h):
        return h.temperature[0]

    def temperature_mid_year(h):
        return h.temperature[1]

    def color_biome(h):
        return h.color_biome

    def color_territories(h):
        return h.color_territories

    def color_satellite(h):
        return h.color_satellite

    def color_features(h):
        if h.has_feature(HexFeature.lava_flow):
            return (200, 100, 0)
        if h.has_feature(HexFeature.volcano):
            return (255, 0, 0)
        if h.has_feature(HexFeature.crater):
            return (255, 255, 0)
        return (200, 200, 200)

    def color_resources(h):
        if h.resource is not None:
            return h.resource.get("type").color
        return (100, 100, 100)

    def color_zone(h):
        return h.zone.color

    def key_zone(h):
        return h.zone.map_key

    def hex_latitude(h):
        return h.latitude

    def color_pressure_end_year(h):
        return h.color_pressure[0]

    def color_pressure_mid_year(h):
        return h.color_pressure[1]

    def pressure_number_end_year(h):
        return h.pressure[0]

    def pressure_number_mid_year(h):
        return h.pressure[1]

    def color_wind_end_year(h):
        return h.color_pressure[0]

    def color_wind_mid_year(h):
        return h.color_pressure[1]

    def wind_display_end_year(h):
        wind = h.wind[0].get("direction")
        if wind:
            return wind.arrow
        return "-"

    def wind_display_mid_year(h):
        wind = h.wind[1].get("direction")
        if wind:
            return wind.arrow
        return "-"

    def color_hex_type(h):
        if h.is_land:
            return (0, 255, 0)
        return (0, 0, 255)

    def color_geoforms(h):
        for g in GeoformType.list():
            if h.geoform.type is g:
                return g.color
        return (0, 0, 255)

    HexGridDraw(
        hex_grid,
        color_features,
        "../output/map_features.png",
        show_coasts=True,
        rivers=False,
    )
    HexGridDraw(
        hex_grid,
        color_heightmap,
        "../output/map_height.png",
        rivers=False,
        show_coasts=True,
    )
    HexGridDraw(
        hex_grid,
        color_terrain,
        "../output/map_terrain.png",
        rivers=True,
        show_coasts=True,
    )
    HexGridDraw(
        hex_grid,
        color_hex_type,
        "../output/map_hex_types.png",
        rivers=True,
        show_coasts=True,
    )
    HexGridDraw(
        hex_grid,
        color_geoforms,
        "../output/map_geoforms.png",
        rivers=False,
        show_coasts=True,
    )
    HexGridDraw(
        hex_grid,
        color_rivers,
        "../output/map_rivers.png",
        rivers=True,
        show_coasts=True,
    )
    HexGridDraw(
        hex_grid,
        color_temperature_end_year,
        "../output/map_temp_end_year.png",
        rivers=False,
        show_coasts=True,
    )
    HexGridDraw(
        hex_grid,
        color_temperature_mid_year,
        "../output/map_temp_mid_year.png",
        rivers=False,
        show_coasts=True,
    )
    HexGridDraw(hex_grid, color_biome, "../output/map_biome.png", rivers=False)
    HexGridDraw(
        hex_grid,
        color_territories,
        "../output/map_territories.png",
        rivers=False,
        show_coasts=True,
        borders=True,
    )
    HexGridDraw(hex_grid, color_satellite, "../output/map_satellite.png")
    HexGridDraw(hex_grid, color_resources, "../output/map_resources.png")
    # HexGridDraw(hex_grid, color_zone, "../output/map_zone.png", text_func=key_zone, rivers=False, show_coasts=False)
    # HexGridDraw(hex_grid, color_zone, "../output/map_latitude.png", text_func=hex_latitude, rivers=False, show_coasts=False)
    # HexGridDraw(hex_grid, color_pressure_end_year, "../output/map_pressure_end_year.png", rivers=False, show_coasts=True)
    # HexGridDraw(hex_grid, color_pressure_mid_year, "../output/map_pressure_mid_year.png", rivers=False, show_coasts=True)
    # HexGridDraw(hex_grid, color_wind_end_year, "../output/map_wind_end_year.png", text_func=wind_display_end_year, rivers=False, show_coasts=True)
    # HexGridDraw(hex_grid, color_wind_mid_year, "../output/map_wind_mid_year.png", text_func=wind_display_mid_year, rivers=False, show_coasts=True)

    # report on territories
    for t in hex_grid.territories:
        print(
            "Territory {}:\n"
            "\tSize: {}\n"
            "\tColor: {}\n"
            "\tLandlocked: {}\n"
            "\tAverage Temperature: {}\n"
            "\tAverage Moisture: {}\n"
            "\tNeighbors: {}".format(
                t.id,
                t.size,
                t.color,
                t.landlocked,
                t.avg_temp,
                t.avg_moisture,
                t.neighbors,
            )
        )
        print("\tBiomes:")
        for b in t.biomes:
            print(
                "\t - {}: {} - {}%".format(
                    b.get("biome").title,
                    b.get("count"),
                    round((b.get("count") / t.size) * 100, 2),
                )
            )
        print("\tGroups: {}".format(len(t.groups)))
        for g in t.groups:
            print("\t\tHexes: {}, X: {}, Y: {}".format(g.get("size"), g.get("x"), g.get("y")))


def generate(params, debug=True, image=True):
    """
    Given a colony, creates a world map
    :param params: generator parameters
    :return: True or False on success
    """
    hex_grid = MapGen(params=params, debug=debug)
    if image:
        draw_grid(hex_grid)
    return hex_grid
