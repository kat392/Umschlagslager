from turtle import pos
from mesa import Agent
from zmq import NULL
from agent import TWare, TLagerplatz, TGabelstapler

class Tagent_routing_controller():
    gabelstapler_waren_zuweisung_dict: dict

    def __init__(self, gabelstapler_list: list[TGabelstapler]) -> None:
        self.gabelstapler_waren_zuweisung_dict = {}
        for gabelstapler in gabelstapler_list:
            self.gabelstapler_waren_zuweisung_dict[gabelstapler] = NULL
        pass

    def step(self, waren_list: list[TWare]):
        # pruefe ob Gabelstapler keine Ware mehr hat
        unreservierte_waren: list[TWare]
        unreservierte_waren = []

        for ware in waren_list:
            if not(ware.ist_reserviert):
                unreservierte_waren.append(ware)
                ware.ist_reserviert = True

        for gabelstapler, ware in self.gabelstapler_waren_zuweisung_dict.items():
            if ware == NULL and len(unreservierte_waren) > 0:
                self.gabelstapler_waren_zuweisung_dict[gabelstapler] = unreservierte_waren[0]
                unreservierte_waren.remove(unreservierte_waren[0])

            if self.gabelstapler_waren_zuweisung_dict[gabelstapler] != NULL and isinstance(self.gabelstapler_waren_zuweisung_dict[gabelstapler], TWare):
                if gabelstapler.next_way_point == NULL:
                    gabelstapler.next_way_point = self.gabelstapler_waren_zuweisung_dict[gabelstapler].pos