import random
import sys
from collections import defaultdict

sys.setrecursionlimit(1500)


class Territory:
    def __init__(self, grid, main, id_num, color):
        self.grid = grid
        self.id = id_num
        self.color = color
        self.main = main  # main Hex
        main.territory = self
        self.last_added = [main]
        self.members = [main]  # Hexes part of this territory
        self.groups = []
        self.db_instance = None

    @property
    def frontier(self):
        """Gets a list of hexes that border this territory that are unowned"""
        frontier = []
        for m in self.last_added:
            frontier.extend([h for h in m.surrounding if h.is_owned is False])
        return frontier

    @property
    def landlocked(self):
        for h in self.members:
            if any([h for h in h.surrounding if h.is_water]):
                return False
        return True

    @property
    def neighbors(self):
        """Returns a set of Territories this territory is next to"""
        terr = set()
        for h in self.members:
            terr.update(
                set([m.territory for m in h.surrounding if m.is_land and m.territory is not None and m.territory.id != self.id])
            )
        return terr

    @property
    def avg_temp(self):
        return round(
            sum([(h.temperature[0] + h.temperature[1]) / 2 for h in self.members]) / self.size,
            2,
        )

    @property
    def avg_moisture(self):
        return round(sum([h.moisture for h in self.members]) / self.size, 2)

    @property
    def biomes(self):
        """Gets a list of biomes and percents"""
        b = dict()
        for h in self.members:
            if h.biome.name in b:
                b[h.biome.name]["count"] += 1
            else:
                b[h.biome.name] = dict(biome=h.biome, count=1)
        return sorted(b.values(), key=lambda k: k["count"], reverse=True)

    def __eq__(self, other):
        return self.id == other.id

    def __key(self):
        return self.id, self.color

    def __hash__(self):
        return hash(self.__key())

    def __repr__(self):
        return "<Territory ID: {}>".format(self.id)

    def find_groups(self):
        """
        Calculates the contiguous groups of hexes in this territory
        :return:
        """
        # print("Territory {}: Members: {}".format(self.id, len(self.members)))

        def find_unmarked():
            # TODO - Make this more sane
            while True:
                found = random.choice(self.members)
                if found.marked is False:
                    return found

        def step(sh, group):
            all_surrounding = set([sh])
            while len(all_surrounding) > 0 and (sh := all_surrounding.pop()):
                if sh.marked:
                    continue
                else:
                    sh.marked = True
                    group.append(sh)
                all_surrounding.update({s for s in sh.map_surrounding if s.is_land and s.territory == self and s.marked is False})

        # def step(sh, group):
        #     if sh.marked:
        #         return
        #     else:
        #         sh.marked = True
        #         group.append(sh)

        #     sur = [
        #         s
        #         for s in sh.map_surrounding
        #         if s.is_land and s.territory is not None and s.territory == self and s.marked is False
        #     ]
        #     # print("\t\tStep into HEX: {}, {} -> Found: {}".format(sh.x, sh.y, len(sur)))
        #     for h in sur:
        #         step(h, group)

        def num_marked():
            return len([h for h in self.members if h.marked])

        groups = []
        while num_marked() < len(self.members):
            # print("\t{} < {}".format(num_marked(), len(self.members)))
            group = []
            sh = find_unmarked()
            step(sh, group)
            groups.append(group)

        # print(groups)
        result = []
        for g in groups:
            mx_s = [h.x for h in g]
            mx = sum(mx_s) / len(mx_s)
            my_s = [h.y for h in g]
            my = sum(my_s) / len(my_s)
            result.append(dict(size=len(g), x=round(mx), y=round(my)))
        self.groups = result

    @property
    def size(self):
        return len(self.members)

    def to_dict(self):
        resources = defaultdict(dict)
        for hex in self.members:
            if hex.resource is not None:
                res_type = hex.resource["type"].title
                res_rating = hex.resource["rating"].title
                if res_rating in resources[res_type]:
                    resources[res_type][res_rating] += 1
                else:
                    resources[res_type][res_rating] = 1
        biomes = []
        for b in self.biomes:
            biomes.append(
                {
                    "title": b["biome"].title,
                    "count": b["count"],
                    "perc": round((b["count"] / self.size) * 100, 2),
                }
            )
        return {
            "id": self.id,
            "size": self.size,
            "color": self.color,
            "landlocked": self.landlocked,
            "average temperature": self.avg_temp,
            "average moisture": self.avg_moisture,
            "resources": resources,
            "neighbors": [n.id for n in self.neighbors],
        }
