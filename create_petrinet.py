from pm4py.objects.petri.petrinet import PetriNet, Marking

net = PetriNet("new_petri_net")

# creating source, p_1 and sink place
source = PetriNet.Place("source")
sink = PetriNet.Place("sink")
p_1 = PetriNet.Place("p_1")

net.places.add(source)
net.places.add(sink)
net.places.add(p_1)

t_1 = PetriNet.Transition("name_1", "label_1")
t_2 = PetriNet.Transition("name_2", "label_2")

net.transitions.add(t_1)
net.transitions.add(t_2)

from pm4py.objects.petri import utils

utils.add_arc_from_to(source, t_1, net)
utils.add_arc_from_to(t_1, p_1, net)
utils.add_arc_from_to(p_1, t_2, net)
utils.add_arc_from_to(t_2, sink, net)

from pm4py.objects.petri.petrinet import Marking

initial_marking = Marking()
initial_marking[source] = 1
final_marking = Marking()
final_marking[sink] = 1

# Exporting
from pm4py.objects.petri.exporter import pnml as pnml_exporter
pnml_exporter.export_net(net, initial_marking, "createdPetriNet1.png", final_marking=final_marking)

#Visualizing
from pm4py.visualization.petrinet import factory as pn_vis_factory

gviz = pn_vis_factory.apply(net, initial_marking, final_marking)
pn_vis_factory.view(gviz)

