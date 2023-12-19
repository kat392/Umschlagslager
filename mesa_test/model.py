from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from agent import TWare, TLagerplatz, TGabelstapler, TWarenEingang, TWarenAusgabe
from agent_routing_controller import Tagent_routing_controller

class OurModel(Model):
    def remove_agent(self, agent):
        self.grid.remove_agent(agent)
        self.schedule.remove(agent)
        self.waren_list.remove(agent)
        agent = None

    def create_agent(self, agent, x_pos = -1, y_pos = -1):
        self.schedule.add(agent)

        if x_pos < 0:
            x_pos = self.random.randrange(self.grid.width)
        if y_pos < 0:
            y_pos = self.random.randrange(self.grid.height)

        self.grid.place_agent(agent, (x_pos, y_pos))
        self.agent_index = self.agent_index + 1

    def create_ware(self, x_pos = -1, y_pos = -1):
        if self.grid.is_cell_empty((x_pos, y_pos)):
            agent = TWare(self.agent_index, self)
            self.create_agent(agent, x_pos, y_pos)
            self.waren_list.append(agent)
        
    def create_lagerplatz(self, x_pos = -1, y_pos = -1):
        agent = TLagerplatz(self.agent_index, self)
        self.create_agent(agent, x_pos, y_pos)
        self.lagerplatz_list.append(agent)

    def create_gabelstapler(self, x_pos = -1, y_pos = -1):
        agent = TGabelstapler(self.agent_index, self)
        self.create_agent(agent, x_pos, y_pos)
        self.gabelstapler_list.append(agent)  

    def create_wareneingang(self, x_pos = -1, y_pos = -1): 
        agent = TWarenEingang(self.agent_index, self, self.create_ware, 5)
        self.create_agent(agent, x_pos, y_pos)
        self.wareneingang_list.append(agent)

    def create_warenausgang(self, x_pos = -1, y_pos = -1): 
        agent = TWarenAusgabe(self.agent_index, self, self.remove_agent)
        self.create_agent(agent, x_pos, y_pos)
        self.warenausgang_list.append(agent)

    def __init__(self, number_agents_gabelstapler, number_agents_lagerplatz, number_agents_ware, width, height):
        self.agent_routing_controller: Tagent_routing_controller

        self.gabelstapler_list: list[TGabelstapler]
        self.lagerplatz_list: list[TLagerplatz]
        self.waren_list: list[TWare]
        self.wareneingang_list: list[TWarenEingang]
        self.warenausgang_list: list[TWarenAusgabe]

        self.gabelstapler_list = []
        self.lagerplatz_list = []
        self.waren_list = []
        self.wareneingang_list = []
        self.warenausgang_list = []

        self.num_agents_gabelstapler = number_agents_gabelstapler
        self.num_agents_lagerplatz = number_agents_lagerplatz
        self.num_agents_ware = number_agents_ware

        self.agent_index = 0
        
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)
        self.running = True

        self.datacollector_currents = DataCollector(
            {
                "Anzahl Gabelstapler": self.num_agents_gabelstapler,
                "Anzahl der Lagerplätze": self.num_agents_lagerplatz,
                "Anzahl der Waren": self.num_agents_ware,
            }
        )        
        for i in range(self.agent_index, self.num_agents_ware + self.agent_index):
            self.create_wareneingang()

        for i in range(self.agent_index, self.num_agents_lagerplatz + self.agent_index):
            self.create_lagerplatz()

        for i in range(self.agent_index, self.num_agents_gabelstapler + self.agent_index):
            self.create_gabelstapler()

        for i in range(self.agent_index, 1 + self.agent_index):
            self.create_warenausgang()

        self.agent_routing_controller = Tagent_routing_controller(self.gabelstapler_list, self.warenausgang_list)

    def step(self):
        """Advance the model by one step."""
        self.agent_routing_controller.step(self.waren_list)
        self.schedule.step()
