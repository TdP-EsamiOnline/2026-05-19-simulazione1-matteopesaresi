import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.artisti = DAO.get_artisti()
        self.mappaArtisti = {artista.ArtistId : artista for artista in self.artisti}
        self.generi = DAO.get_generi()
        self.grafo = nx.DiGraph()
    def buildGraph(self,genere):
        self.grafo.clear()

        # 1. Aggiungiamo i NODI (oggetti) pescandoli dalla idMap
        self.vertici = DAO.get_vertici(genere)
        for v_id in self.vertici:
            self.grafo.add_node(self.mappaArtisti[v_id])

        # 2. Calcoliamo la popolarità e raccogliamo i clienti di ogni artista
        self.vendite = DAO.get_artist_track(genere)

        popolarita = {v_id: 0 for v_id in self.vertici}
        clienti = {v_id: set() for v_id in self.vertici}

        for riga in self.vendite:
            id_art = riga["id"]
            popolarita[id_art] += riga["qt"]
            clienti[id_art].add(riga["customer"])
            # 3. Creiamo gli ARCHI (doppio ciclo for per confrontare le coppie)
        for u_id in self.vertici:
            for v_id in self.vertici:
                if u_id != v_id:
                    # Controlliamo se hanno clienti in comune (intersezione tra i due set)
                    clienti_in_comune = clienti[u_id].intersection(clienti[v_id])

                    if len(clienti_in_comune) > 0:
                        # C'è l'arco! Calcoliamo il peso
                        peso = popolarita[u_id] + popolarita[v_id]
                        nodo_u = self.mappaArtisti[u_id]
                        nodo_v = self.mappaArtisti[v_id]

                        # Decidiamo il verso: da chi ha pop > verso chi ha pop <
                        if popolarita[u_id] > popolarita[v_id]:
                            self.grafo.add_edge(nodo_u, nodo_v, weight=peso)
                        elif popolarita[u_id] == popolarita[v_id]:
                            # Se uguali, va in entrambi i versi (per non duplicarli col doppio ciclo, ci penserà NetworkX)
                            self.grafo.add_edge(nodo_u, nodo_v, weight=peso)

    def get_number_nodes(self):
        return len(self.grafo.nodes)

    def get_number_edge(self):
        return len(self.grafo.edges)

    def get_artista_piu_influente(self):
        # Influenza = peso archi uscenti - peso archi entranti
        if len(self.grafo.nodes) == 0:
            return None, 0

        best_artista = None
        max_influenza = -float('inf')

        for nodo in self.grafo.nodes:
            peso_uscenti = sum([data['weight'] for u, v, data in self.grafo.out_edges(nodo, data=True)])
            peso_entranti = sum([data['weight'] for u, v, data in self.grafo.in_edges(nodo, data=True)])

            influenza = peso_uscenti - peso_entranti

            if influenza > max_influenza:
                max_influenza = influenza
                best_artista = nodo

        return best_artista, max_influenza

    def get_top_5_archi(self):
        archi = []
        for u, v, data in self.grafo.edges(data=True):
            archi.append((u, v, data['weight']))

        # Ordiniamo in modo decrescente basandoci sul peso (x[2])
        archi.sort(key=lambda x: x[2], reverse=True)
        return archi[:5]

    def trova_cammino(self, id_start):
        nodo_start = self.mappaArtisti.get(id_start)
        if nodo_start not in self.grafo.nodes:
            return []
            
        self._best_path = []
        
        self._ricorsione(nodo_start, [nodo_start], -1)
        
        return self._best_path

    def _ricorsione(self, nodo_corrente, path_corrente, peso_precedente):
        if len(path_corrente) > len(self._best_path):
            self._best_path = list(path_corrente)
            
        for vicino in self.grafo.successors(nodo_corrente):
            if vicino not in path_corrente:
                peso_arco = self.grafo[nodo_corrente][vicino]['weight']
                if peso_arco > peso_precedente:
                    path_corrente.append(vicino)
                    self._ricorsione(vicino, path_corrente, peso_arco)
                    path_corrente.pop()
