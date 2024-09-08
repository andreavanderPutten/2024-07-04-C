import flet as ft
from UI.view import View
from database.DAO import DAO
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        anno = int(self._view.ddyear.value)
        forma = self._view.ddshape.value
        if anno == None or forma == None :
            self._view.create_alert("Non hai scelto uno tra l' anno e la forma")
        self._model.creaGrafo(forma,anno)
        self._view.txt_result1.controls.append(ft.Text(f"Numero di nodi : {self._model.grafoDetails()[0]},Numero di archi : {self._model.grafoDetails()[1]}"))
        top5 = self._model.top5()
        for elemento in top5 :
            self._view.txt_result1.controls.append(ft.Text(f"{elemento[0].id} --> {elemento[1].id} : | weight :{elemento[2]["weight"]}"))

        self._view.update_page()

    def handle_path(self, e):
        percorso_migliore,score = self._model.cammino_migliore()

        self._view.txt_result2.controls.append(ft.Text(f"Il percorso migliore ha valore {score}"))
        for elemento in percorso_migliore :
            self._view.txt_result2.controls.append(ft.Text(elemento))

        self._view.update_page()
    def fillDD(self):
        anni = DAO.getAnni()
        self._view.ddyear.options = list(map(lambda x: ft.dropdown.Option(x), anni))
    def handle_change(self,e):
        anno = int(self._view.ddyear.value)
        forme = DAO.getForme(anno)
        for forma in forme :
            if forma == "" :
                forme.remove(forma)
        self._view.ddshape.options = list(map(lambda x: ft.dropdown.Option(x), forme))
        self._view.update_page()