import copy

from database.DAO import DAO
import networkx as nx

from model.sighting import Sighting


class Model:
    def __init__(self):
        self.grafo = nx.DiGraph()
        self.nodi = []
        self.idMap = {}
        self.migliore_percorso = []
        self.best_score = 0
        self.occorrenze_mese = dict.fromkeys(range(1, 13), 0)
    def creaGrafo(self,forma,anno):
        self.nodi = DAO.getNodi(anno,forma)
        for nodo in self.nodi :
            self.idMap[nodo.id] = nodo
        self.grafo.add_nodes_from(self.nodi)
        lista_archi = DAO.getArchi(anno,forma,self.idMap)
        for coppia in lista_archi:
            lon1 = coppia[0].longitude
            lon2 = coppia[1].longitude
            if lon1 > lon2:
                self.grafo.add_edge(coppia[1], coppia[0], weight=lon1 - lon2)
            elif lon1 < lon2:
                self.grafo.add_edge(coppia[0], coppia[1], weight=lon2 - lon1)

    def grafoDetails(self):
        return len(self.grafo.nodes), len(self.grafo.edges)

    def top5(self):
        sorted_edges = sorted(self.grafo.edges(data=True), key=lambda edge: edge[2].get('weight'), reverse=True)
        return sorted_edges[0:5]

    def cammino_migliore(self):
        self.migliore_percorso = []
        self.best_score = 0
        self._occorrenze_mese = dict.fromkeys(range(1, 13), 0)

        for nodo in self.nodi :
            self.occorrenze_mese[nodo.datetime.month] += 1
            successivi = self.successivi_ammissibili(nodo)
            self.ricorsione([nodo],successivi)
            self.occorrenze_mese[nodo.datetime.month] -= 1
        return self.migliore_percorso, self.best_score


    def ricorsione(self,parziale : list[Sighting], successivi : list[Sighting]):
        if len(successivi) == 0 :
            score = Model.calcola_cammino(parziale)
            if score > self.best_score :
                self.best_score = score
                self.migliore_percorso = copy.deepcopy(parziale)
        else :
            for nodo in successivi:
                parziale.append(nodo)
                self.occorrenze_mese[nodo.datetime.month] += 1
                nuovi_succ = self.successivi_ammissibili(nodo)
                self.ricorsione(parziale, nuovi_succ)
                self.occorrenze_mese[parziale[-1].datetime.month] -= 1
                parziale.pop()
    def successivi_ammissibili(self, nodo : Sighting):
        successivi = self.grafo.neighbors(nodo)
        ammissibili = []
        for succ in successivi :
            if succ.duration > nodo.duration and self.occorrenze_mese[succ.datetime.month] < 3 :
                ammissibili.append(succ)
        return ammissibili

    @staticmethod
    def calcola_cammino(cammino : list[Sighting]):
        score = 100*len(cammino)
        for i in range(1,len(cammino)) :
            if cammino[i].datetime.month == cammino[i-1].datetime.month :
                score += 200
        return score
