from turtle import pos
from mesa import Agent
from agent import TWare, TLagerplatz, TGabelstapler, TWarenAusgabe

class Tagent_routing_controller():
    gabelstapler_list: list[TGabelstapler]

    def __init__(self, gabelstapler_list: list[TGabelstapler], warenausgabe: TWarenAusgabe) -> None:
        self.warenausgabe = warenausgabe
        self.gabelstapler_list = gabelstapler_list

    def find_next_way_point_for_gabelstapler(self, gabelstapler: TGabelstapler):
        if gabelstapler.reservierte_ware_ist_beladen():
            # Gabelstapler hat Ware geladen/muss seine abliefern
            gabelstapler.next_way_point = self.warenausgabe.pos
        else:
            # Gabelstapler hat keine Ware geladen/muss welche besorgen
            if gabelstapler.reservierte_ware is not None:
                gabelstapler.next_way_point = gabelstapler.reservierte_ware.pos
            else:
                gabelstapler.next_way_point = (0, 0)


    def step(self, waren_list: list[TWare]):
        unreservierte_waren: list[TWare]
        unreservierte_waren = []

        #reservieren
        for ware in waren_list:
            if ware.reservierer is None:
                unreservierte_waren.append(ware)

        for gabelstapler in self.gabelstapler_list:
            if gabelstapler.reservierte_ware is None and len(unreservierte_waren) > 0:
                ware = unreservierte_waren[0]
                gabelstapler.reservierte_ware = ware
                ware. reservierer = gabelstapler
                unreservierte_waren.remove(ware)

            self.find_next_way_point_for_gabelstapler(gabelstapler)
            

                
            '''
        for gabelstapler in self.gabelstapler_list:
            # Wenn Gabelstapler keine Ware hat und Waren noch nicht reserviert sind
            if (ware is None) and len(unreservierte_waren) > 0:
                # Gabelstapler reserviert spezifisch eine Ware
                self.gabelstapler_waren_zuweisung_dict[gabelstapler] = unreservierte_waren[0]
                ware = unreservierte_waren[0]
                ware.reservierer = gabelstapler
                unreservierte_waren.remove(unreservierte_waren[0])

            if gabelstapler.next_way_point is None:
                self.find_next_way_point_for_gabelstapler(gabelstapler, ware)
                '''