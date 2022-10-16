from kivymd.app import MDApp 
from kivy.lang import Builder
from kivy_garden.graph import Graph, LinePlot
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.pickers import MDDatePicker
import json

###GLOBALE FUNKTIONEN###

def open_json(filename):
    f = open(filename)
    json_obj = json.load(f)
    f.close()
    return json_obj

def write_runde(new_data, filename="runde.json"):
    with open(filename,'r+') as file:
        file_data = json.load(file)
        file_data["gespielte_runde"].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent = 4)

def write_kurs(new_data, filename="course.json"):
    with open(filename,'r+') as file:
        file_data = json.load(file)
        file_data["platz"].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent = 4)

def calc_nine(data):
    data["var_neu"] = 18
    data["schlag_neu"] = data["schlaege"]*2 + 1
    data["netto_punkte_neu"] = data["netto_punkte"]*2 -1
    data["hochgerechnet"] = True
    return data

def kurs_par():
    json_runde = open_json("runde.json")
    json_course = open_json("course.json")
    num_par = []
    ges_platz = []
    for item in range(len(json_runde["gespielte_runde"])):
        ges_platz.append(json_runde["gespielte_runde"][item]["golfplatz"])
    for item in ges_platz:
        num_par.append(json_course[item]["par"])
    return num_par

def input_data_runde(data):
    if data["variante"] == 9:
        write_runde(calc_nine(data))
    else:
        write_runde(data)

###################

class Output(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.plot_graph()

    def update_stat(self):
        upt_punkt = self.d_punkt()
        upt_schlag = self.d_schlag()
        upt_spiel = int(self.anz_spiel()) -1
        self.ids.lbl_punkt.text = upt_punkt
        self.ids.lbl_schlag.text = upt_schlag
        self.ids.lbl_spiel.text = str(upt_spiel)

    def update_graph(self):
        try:
            self.ids.graph.remove_widget(self.graph)
            self.plot_graph()
        except:
            pass

    def plot_graph(self):
        try:
            self.score, self.schlaege = self.get_graph_data()
            self.graph = Graph(
            x_grid=True, y_grid = True,
            x_grid_label=True,y_grid_label=True,
            border_color=[0,0,0,1],
            xmax = len(self.score),
            ymax = max(self.schlaege)+ 30,
            x_ticks_major = 1,
            y_ticks_major = 20,
            ymin = 0,
            background_color=[100,100,100,0.7]
            )
            self.ids.graph.add_widget(self.graph)
            self.plot_schlaege = LinePlot(line_width=2,color=[1, 0, 0, 1])
            self.plot_score = LinePlot(line_width=2,color=[1, 1, 0, 1])
            self.plot_score.points = [(day, self.score[day]) for day in range(len(self.score))]
            self.plot_schlaege.points = [(day, self.schlaege[day]) for day in range(len(self.schlaege))]
            self.graph.add_plot(self.plot_schlaege)
            self.graph.add_plot(self.plot_score)
        except:
            pass

    def get_graph_data(self):
        try:
            json_runde = open_json("runde.json")
            score = []
            day = []
            schlaege = []

            for item in range(len(json_runde["gespielte_runde"])):
                if json_runde["gespielte_runde"][item]["hochgerechnet"]:
                    score.append(json_runde["gespielte_runde"][item]["netto_punkte_neu"])
                    schlaege.append(json_runde["gespielte_runde"][item]["schlag_neu"])
                else:
                    score.append(json_runde["gespielte_runde"][item]["netto_punkte"])
                    schlaege.append(json_runde["gespielte_runde"][item]["schlaege"])
                day.append(json_runde["gespielte_runde"][item]["datum"]) 

            return score, schlaege
        except:
            pass
    
    def d_schlag(self):
        try:
            json_runde = open_json("runde.json")
            summe_schlaege = 0

            for item in range(len(json_runde["gespielte_runde"])):
                if json_runde["gespielte_runde"][item]["hochgerechnet"]:
                    summe_schlaege += json_runde["gespielte_runde"][item]["schlag_neu"]
                else:
                    summe_schlaege += json_runde["gespielte_runde"][item]["schlaege"]
            durchschnitt_schlaege = summe_schlaege//(len(json_runde["gespielte_runde"]))
            return str(durchschnitt_schlaege)
        except:
            return str(0)

    def d_punkt(self):
        try:
            json_runde = open_json("runde.json")
            summe_punkte = 0

            for item in range(len(json_runde["gespielte_runde"])):
                if json_runde["gespielte_runde"][item]["hochgerechnet"]:
                    summe_punkte += json_runde["gespielte_runde"][item]["netto_punkte_neu"]
                else:
                    summe_punkte += json_runde["gespielte_runde"][item]["netto_punkte"]
            durchschnitt_punkte = summe_punkte//(len(json_runde["gespielte_runde"]))
            return str(durchschnitt_punkte)

        except:
            return str(0)

    def anz_spiel(self):
        try:
            json_runde = open_json("runde.json")
            i = 0
            for item in range(len(json_runde["gespielte_runde"])):
                i += 1
            return str(i)
        except:
            return str(0)

class RundeScreen(Screen):

    def on_save(self, instance, value, range):
        self.ids.datum_input.text = str(value)

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def get_course(self):
        self.json_course = open_json("course.json")
        return self.json_course.keys()

    def submit(self):
        data = { "datum": self.ids.datum_input.text,
         "golfplatz": self.ids.platz_spinner.text,
         "variante": int(self.ids.variante_spinner.text),
         "abschlag": self.ids.abschlag_spinner.text,
         "schlaege": int(self.ids.schlag_input.text),
         "netto_punkte": int(self.ids.punkte_input.text),
         "handicap": int(self.ids.hcp_input.text),
         "hochgerechnet": False
        }
        input_data_runde(data)
        Output().update_stat()

    def clear_input(self):
        self.ids.datum_input.text = ""
        self.ids.platz_spinner.text = "Golfplatz"
        self.ids.variante_spinner.text = "Variante"
        self.ids.abschlag_spinner.text = "Abschlag"
        self.ids.schlag_input.text = ""
        self.ids.punkte_input.text = ""
        self.ids.hcp_input.text = ""

class PlatzScreen(Screen):

    def clear_input(self):
        self.ids.course_name.text = ""
        self.ids.course_par.text = ""
        self.ids.variante_spinner.text = "9 oder 18-Löcher"
        self.ids.course_rating_m.text = ""
        self.ids.course_rating_w.text = ""
        self.ids.course_slope_m.text = ""
        self.ids.course_slope_w.text = ""

    def submit(self):
        data = { "name": self.ids.course_name.text,
            "par": int(self.ids.course_par.text),
            "loch_anz": int(self.ids.variante_spinner.text),
            "rating_herren_gelb": int(self.ids.course_rating_m.text),
            "rating_damen_rot": int(self.ids.course_rating_w.text),
            "slope_herren_gelb": int(self.ids.course_slope_m.text),
            "slope_damen_rot": int(self.ids.course_slope_w.text)
            }
        write_kurs(data)

class MyApp(MDApp):

    def build(self): 

        sm = ScreenManager()
        sm.add_widget(Output(name='output'))
        sm.add_widget(RundeScreen(name='runde'))
        sm.add_widget(PlatzScreen(name='platz'))

        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = 'BlueGray'

        return sm

if __name__ == "__main__":
    MyApp().run()










