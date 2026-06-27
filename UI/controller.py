import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDGenre(self):
        # Punto 1.a: Riempiamo la tendina con i generi all'avvio
        for g in self._model.generi:
            self._view._ddGenre.options.append(ft.dropdown.Option(g))
        self._view.update_page()

    def handleCreaGrafo(self, e):
        # Leggiamo il valore selezionato
        genere = self._view._ddGenre.value

        if genere is None:
            self._view.create_alert("Per favore, seleziona un genere prima di creare il grafo!")
            return

        # Puliamo lo schermo
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Creazione grafo in corso per il genere: {genere}..."))
        self._view.update_page()

        # 1. PUNTO 1.b: Chiamiamo il model per creare il grafo
        self._model.buildGraph(genere)

        # 2. PUNTO 1.c: Stampiamo i risultati statistici
        n_nodi = self._model.get_number_nodes()
        n_archi = self._model.get_number_edge()

        self._view.txt_result.controls.append(
            ft.Text("Grafo correttamente creato:", color="green", weight=ft.FontWeight.BOLD))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {n_nodi}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {n_archi}"))

        best_artista, influenza = self._model.get_artista_piu_influente()
        if best_artista:
            self._view.txt_result.controls.append(
                ft.Text(f"Artista più influente: {best_artista.Name}, con influenza: {influenza}")
            )

        self._view.txt_result.controls.append(ft.Text("\nTop 5 archi:"))
        top_archi = self._model.get_top_5_archi()
        for u, v, peso in top_archi:
            self._view.txt_result.controls.append(ft.Text(f"{u.Name} -> {v.Name} : {peso}"))

        # 3. PREPARAZIONE PUNTO 2: Popoliamo la tendina degli artisti
        self._view._ddArtist.options.clear()  # Svuotiamo se c'erano vecchi artisti

        for nodo in self._model.grafo.nodes:
            # key: quello che il programma legge dietro le quinte (l'ID)
            # text: quello che l'utente vede a schermo (il Nome)
            self._view._ddArtist.options.append(ft.dropdown.Option(
                key=str(nodo.ArtistId),
                text=nodo.Name
            ))

        self._view.update_page()

    def handleCammino(self, e):
        artist_id_str = self._view._ddArtist.value
        if artist_id_str is None:
            self._view.create_alert("Per favore, seleziona un artista prima di cercare il cammino!")
            return
            
        artist_id = int(artist_id_str)
        
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Calcolo del cammino in corso..."))
        self._view.update_page()
        
        path = self._model.trova_cammino(artist_id)
        
        self._view.txt_result.controls.clear()
        if not path:
            self._view.txt_result.controls.append(ft.Text("Nessun cammino trovato o artista non valido.", color="red"))
        else:
            self._view.txt_result.controls.append(ft.Text(f"Cammino trovato (Lunghezza: {len(path)-1} archi, {len(path)} nodi):", weight="bold", color="green"))
            for i, nodo in enumerate(path):
                self._view.txt_result.controls.append(ft.Text(f"{i+1}. {nodo.Name}"))
                
        self._view.update_page()