from mesa import Agent
from zmq import NULL
from agent import TWare, TLagerplatz, TGabelstapler

class Tagent_routing_controller():
    def __init__(self) -> None:
        pass

    def finde_naehste_freie_ware(self, gabelstapler: TGabelstapler, waren_list: list[TWare]):
        for ware in waren_list:
            gabelstapler.ware = ware
            break

    def step(self, agent_list: list[Agent]):
        # Get Agents die hier gebraucht werden und speichere sie in gecastete listen
        waren_list: list[TWare]
        gabelstapler_list: list[TGabelstapler]

        waren_list = []
        gabelstapler_list = []

        for agent in agent_list:
            if isinstance(agent, TWare):
                waren_list.append(agent)
            if isinstance(agent, TGabelstapler):
                gabelstapler_list.append(agent)

        # pruefe ob Gabelstapler keine Ware mehr hat
        for gabelstapler in gabelstapler_list:
            if gabelstapler.ware == NULL:
                self.finde_naehste_freie_ware(gabelstapler, waren_list)



    
    
    
    

        