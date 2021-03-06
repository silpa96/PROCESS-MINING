from pm4py.objects.dfg.utils import dfg_utils
from pm4py.algo.discovery.inductive import factory as initial
from pm4py.objects.petri.petrinet import PetriNet, Marking
from pm4py.objects.petri import utils as pn_util
from enum import Enum
from pm4py.util import exec_utils

class Parameters(Enum):
    START_ACTIVITIES = 'start_activities'
    END_ACTIVITIES = 'end_activities'


PARAM_KEY_START_ACTIVITIES = Parameters.START_ACTIVITIES
PARAM_KEY_END_ACTIVITIES = Parameters.END_ACTIVITIES

class Custom:

    def __init__(self,log,dfg,s,e,sel):
        self.log=log
        self.dfg=dfg
        self.s=s
        self.e=e
        self.initializer=initial
        self.sel=sel

    def get_plot(self,parameters=None):
        dfg=self.dfg
        s=self.s
        e=self.e

        
        if parameters is None:
            parameters = {}

        dfg = dfg
        start_activities = s
        end_activities =e
        activities = dfg_utils.get_activities_from_dfg(dfg)

        net = PetriNet("")
        im = Marking()
        fm = Marking()
        source = PetriNet.Place("source")
        net.places.add(source)
        im[source] = 1
        sink = PetriNet.Place("sink")
        net.places.add(sink)
        fm[sink] = 1

        places_corr = {}
        index = 0

        for act in activities:
            places_corr[act] = PetriNet.Place(act)
            net.places.add(places_corr[act])

        for act in start_activities:
            if act in places_corr:
                index = index + 1
                trans = PetriNet.Transition(act + "_" + str(index), act)
                net.transitions.add(trans)
                pn_util.add_arc_from_to(source, trans, net)
                pn_util.add_arc_from_to(trans, places_corr[act], net)

        for act in end_activities:
            if act in places_corr:
                index = index + 1
                inv_trans = PetriNet.Transition(act + "_" + str(index), None)
                net.transitions.add(inv_trans)
                pn_util.add_arc_from_to(places_corr[act], inv_trans, net)
                pn_util.add_arc_from_to(inv_trans, sink, net)

        for el in dfg.keys():
            act1 = el[0]
            act2 = el[1]

            index = index + 1
            trans = PetriNet.Transition(act2 + "_" + str(index), act2)
            net.transitions.add(trans)

            pn_util.add_arc_from_to(places_corr[act1], trans, net)
            pn_util.add_arc_from_to(trans, places_corr[act2], net)

        return net, im, fm

    def apply(self):
        dfg=self.dfg
        s=self.s
        e=self.e
        parameters = {}

        dfg = dfg
        start_activities = s
        end_activities =e
        activities = dfg_utils.get_activities_from_dfg(dfg)

        net = PetriNet("")
        im = Marking()
        fm = Marking()
        source = PetriNet.Place("source")
        net.places.add(source)
        im[source] = 1
        sink = PetriNet.Place("sink")
        net.places.add(sink)
        fm[sink] = 1

        places_corr = {}
        index = 0

        for act in activities:
            places_corr[act] = PetriNet.Place(act)
            net.places.add(places_corr[act])

        for act in start_activities:
            if act in places_corr:
                index = index + 1
                trans = PetriNet.Transition(act + "_" + str(index), act)
                net.transitions.add(trans)
                pn_util.add_arc_from_to(source, trans, net)
                pn_util.add_arc_from_to(trans, places_corr[act], net)

        for act in end_activities:
            if act in places_corr:
                index = index + 1
                inv_trans = PetriNet.Transition(act + "_" + str(index), None)
                net.transitions.add(inv_trans)
                pn_util.add_arc_from_to(places_corr[act], inv_trans, net)
                pn_util.add_arc_from_to(inv_trans, sink, net)

        for el in dfg.keys():
            act1 = el[0]
            act2 = el[1]

            index = index + 1
            trans = PetriNet.Transition(act2 + "_" + str(index), act2)
            net.transitions.add(trans)

            pn_util.add_arc_from_to(places_corr[act1], trans, net)
            pn_util.add_arc_from_to(trans, places_corr[act2], net)

        return self.net, self.im, self.fm
            

    def initialize(self):
        log=self.log
        inf=self.initializer
        n,im,fm=inf.apply(self.log)
        self.net=n
        self.im=im
        self.fm=fm
        
