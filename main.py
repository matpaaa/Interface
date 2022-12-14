from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivy.lang import Builder
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton
from kv import KV
from data import DataBase


class MainApp(MDApp,Screen):
    def build(self):
        # Met le theme dark et la couleur en rouge
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"

        # Ajoute tous l'interface au screen Principal
        self.screen = Screen()
        self.app_screen = Builder.load_string(KV)
        self.screen.add_widget(self.app_screen)

        self.db = DataBase("Data.db")
        #self.label = []
        #self.textfield = []
        self.lang = "an"

        # Initialize la base de données
        self.init_data_table = True

        # Crée la Data Table pour la première page
        self.values_data_table = []
        self.create_data_table()

        return self.screen

    def create_data_table(self) -> None:
        # Crée la Data Table de la premiere page
        #[("ID",5),("Prefixe",20),("Bots",40),("ID_Bots",75),("Status",30),("Ping",15),("Joue à",30),("En Ligne",25),("Next Status",30),("Token",100)]
        self.data_tables = MDDataTable(size_hint=(.9,.7), elevation=3, rows_num=20,column_data=[("ID",5),("Prefixe",40),("Bots",40),("ID_Bots",75),("Status",30),("Ping",15),("Joue à",30),("En Ligne",25),("Next Status",30)],row_data=self.values_data_table)
        if self.init_data_table:
            self.init_data_table = False
            if len(self.db.fetch_all()) != 0:
                for values in self.get_all_data():
                    self.data_tables.add_row(values)
                self.values_data_table = self.get_all_data()
        self.data_tables.bind(on_row_press=self.open_dialog)
        self.app_screen.ids.bot.add_widget(self.data_tables)

    def press(self,x,prefix=None) -> None:
        if x == "add":
            # Bouton ajouter un bot
            self.db.insert(prefix,self.app_screen.ids.name.text,self.app_screen.ids.id.text,"status","ping","Joue à","En ligne","Next Status",self.app_screen.ids["token"].text)
            self.data_tables.row_data = (self.get_all_data())
            for i in ["id","name","prefix","token"]:
                self.app_screen.ids[i].text = ""

        elif x == "delete-all":
            # Bouton tous supprimer
            self.db.delete("all_row",self.data_tables)
        elif x == "delete_id":
            # Bouton supprimer avec l'ID
            if self.check_id(self.app_screen.ids["id_delete"].text):
                self.db.delete("id",self.data_tables,self.app_screen.ids["id_delete"].text)
                self.data_tables.row_data = (self.get_all_data())
                self.app_screen.ids["id_delete"].text = ""
                """
                for i in self.db.fetch_all():
                    print(i)
                    self.db.update_id()
                    self.data_tables.row_data = (self.get_all_data())
                    print(self.get_all_data())
                    self.app_screen.ids["id_delete"].text = "" 
                    """
            else:
                _lang = {"fr":"S'il vous plait entrer un ID qui existe","an":"Please Enter ID who exist","po":"Insira um ID que exista"}
                self.app_screen.ids["id_delete"].text = _lang.get(self.lang)
        elif x == "change_prefix":
            if self.app_screen.ids["id_change"].text == "":
                _lang2 = {"fr":"Veuillez entrer l'ID pour changer le préfixe","an":"Please Enter ID For change Prefix","po":"Insira o ID para alterar o prefixo"}
                self.app_screen.ids["id_change"].text = _lang2.get(self.lang)
            self.db.update(self.app_screen.ids["id_change"].text,self.app_screen.ids["prefix_change"].text)
            self.data_tables.row_data = (self.get_all_data())

    def change_language(self,language) -> None:
        if language == "francais":
            self.lang = "fr"
            for id,text in zip(["prefix","name","id","token","id_delete","prefix_change"],["Entrer un préfixe","Entrer un nom","Entrer un ID","Entrer un token","Entrer un ID pour supprimer","Entrer un ID","Entrer un nouveau prefixe"]):
                self.app_screen.ids[id].hint_text = text
            for id,text in zip(["fr","an","po","new_prefixe","remove_id","remove_all","onglet2","onglet3"],["Français","Anglais","Portugais","Ajouter un nouveau préfixe","Supprimer avec l'identifiant","Supprimer toute les lignes","Ajouter-un-Bots","Changer-la-lang"]):
                self.app_screen.ids[id].text = text
        elif language == "anglais":
            self.lang = "an"
            for id,text in zip(["prefix","name","id","token","id_delete","prefix_change"],["Enter prefix","Enter name","Enter ID","Enter Token","Enter ID for delete","Enter ID","Enter a new prefix"]):
                self.app_screen.ids[id].hint_text = text
            for id,text in zip(["fr","an","po","new_prefixe","remove_id","remove_all","onglet2","onglet3"],["French","English","Portuguese","Add a new prefix","Delete with ID","Delete all row","Add-Bots","Change-Lang"]):
                self.app_screen.ids[id].text = text
        elif language == "portugais":
            self.lang = "po"
            for id,text in zip(["prefix","name","id","token","id_delete","prefix_change"],["Inserir prefixo","Inserir nome","Inserir ID","Inserir token","Inserir ID para excluir","Inserir ID","Inserir um novo prefixo"]):
                self.app_screen.ids[id].hint_text = text
            for id,text in zip(["fr","an","po","new_prefixe","remove_id","remove_all","onglet2","onglet3"],["Francês","Inglês","Português","Adicionar novo prefixo","Excluir com id","Excluir todas as linhas","Adicionar-Bots","Alterar-Idioma"]):
                self.app_screen.ids[id].text = text

    def open_dialog(self,table,row) -> None:
        # Ouvre le dialog
        start_index, end_index = row.table.recycle_data[row.index]["range"]
        if start_index == 0:
            index = 0
        elif start_index == 9:
            index = 1
        else:
            index = int(start_index/6-1)
        self.dialog = MDDialog(title="Config Bots",text=f"Prefixe : {self.db.fetch_all()[index][1]}\nName : {self.db.fetch_all()[index][2]}\nID : {self.db.fetch_all()[index][3]}\nStatus : {self.db.fetch_all()[index][4]}\nPing : {self.db.fetch_all()[index][5]}\nJoue à : {self.db.fetch_all()[index][6]}\nEn ligne : {self.db.fetch_all()[index][7]}\nNext Status : {self.db.fetch_all()[index][8]}",buttons=[MDRectangleFlatButton(text="Close", on_press=self.close_dialog,),MDRectangleFlatButton(text="Start",on_press=self.start_bot)])
        self.dialog.open()

    def close_dialog(self,instance) -> None:
        # Ferme la boite de dialog
        self.dialog.dismiss()

    def start_bot(self,instance):
        # Demarre le bot
        instance.text = "Stop"
        pass

    def get_all_data(self) -> list[list[str,...]]:
        data = []
        for i in self.db.fetch_all():
            x = list(i)
            del x[-1]
            data.append(x)
        return data

    def check_id(self,x) -> bool:
        for i in self.db.fetch_all():
            return (True if i[3] == x else False)


MainApp().run()