from kivymd.app import MDApp
from kivy.lang import Builder

import recommend as r

kv = """
Screen:
    MDLabel:
        text: ""
        id: txt
        pos_hint: {'center_x': 0.5, 'center_y': 0.8}
    MDLabel:
        text: "Welcome to the recommendation system! This system is built from SVD and trained by Retail " \
                     "Rocket dataset, press any button to start. Please press the 3 buttons on the top to " \
                     "tell us your point of view to this item. You can also skip item by pressing the 'skip this' " \
                     "button."
        id: welcome
        pos_hint: {'center_x': 0.5, 'center_y': 0.8}
    MDLabel:
        text: ""
        id: goodbye
        pos_hint: {'center_x': 0.5, 'center_y': 0.6}
    MDLabel:
        text: ""
        id: recommend
        pos_hint: {'center_x': 0.5, 'center_y': 0.6} 
    MDRaisedButton:
        text: 'take a glance'
        pos_hint: {'center_x': 0.35, 'center_y': 0.3}
        on_press:
            app.view()
    MDRaisedButton:
        text: 'add to cart'
        pos_hint: {'center_x': 0.5, 'center_y': 0.3}
        on_press:
            app.add()
    MDRaisedButton:
        text: 'buy it now!'
        pos_hint: {'center_x': 0.65, 'center_y': 0.3}
        on_press:
            app.buy()
    MDRaisedButton:
        text: 'end browsing'
        pos_hint: {'center_x': 0.5, 'center_y': 0.2}
        on_press:
            app.recommend()
    MDRaisedButton:
        text: 'skip this'
        pos_hint: {'center_x': 0.35, 'center_y': 0.2}
        on_press:
            app.skip()
    MDRaisedButton:
        text: 'reset all'
        pos_hint: {'center_x': 0.65, 'center_y': 0.2}
        on_press:
            app.reset()   
                     
"""


class Main(MDApp):
    item_id = 0

    def build(self):
        return Builder.load_string(kv)

    def clear(self):
        labels = []
        labels.append(self.root.ids.recommend)
        labels.append(self.root.ids.txt)
        labels.append(self.root.ids.welcome)
        labels.append(self.root.ids.goodbye)
        for label in labels:
            label.text = ""

    def generate(self):
        self.item_id = r.randomRecommend()
        label = self.root.ids.recommend
        label.text = "The ID of this item is: " + str(self.item_id) + " ."

    def handle(self):
        self.clear()
        label = self.root.ids.txt
        label.text = "seems you have not generate item to interact with. No worries, the item is generated now. Press " \
                     "'skip this' to skip this item, and 'end browse' to get recommendations "
        self.generate()

    def view(self):
        if self.item_id != 0:
            self.clear()
            label = self.root.ids.txt
            label.text = "Action recorded. Generating next item. Press 'skip this' to skip this item, and 'end " \
                         "browse' to get recommendations"
            r.recordData(self.item_id, 1)
            self.generate()
        else:
            self.handle()

    def add(self):
        if self.item_id != 0:
            self.clear()
            label = self.root.ids.txt
            label.text = "Action recorded. Generating next item. Press 'skip this' to skip this item, and 'end " \
                         "browse' to get recommendations"
            r.recordData(self.item_id, 3)
            self.generate()
        else:
            self.handle()

    def buy(self):
        if self.item_id != 0:
            self.clear()
            label = self.root.ids.txt
            label.text = "Action recorded. Generating next item. Press 'skip this' to skip this item, and 'end " \
                         "browse' to get recommendations"
            r.recordData(self.item_id, 6)
            self.generate()
        else:
            self.handle()

    def skip(self):
        if self.item_id != 0:
            self.clear()
            label = self.root.ids.txt
            label.text = "Generating next item. Press 'skip this' to skip this item"
            self.generate()
        else:
            self.handle()

    def reset(self):
        if self.item_id != 0:
            self.clear()
            label = self.root.ids.txt
            label.text = "Personal data reset. Generating first item."
            r.initial = [[], []]
            self.generate()
        else:
            self.handle()

    def recommend(self):
        if self.item_id != 0:
            self.clear()
            recommends = r.recommend(r.initial)
            label = self.root.ids.txt
            label2 = self.root.ids.goodbye
            label.text = "these are the items that you may interested in: " + str(recommends[0]) + ", " + str(
                recommends[1]) + ", " + str(recommends[2]) + " ."
            label2.text = "Thank you for using the recommendation system. You can keep finding new items by pressing " \
                          "'skip this' button, or clear all existing personal data by pressing 'reset all' button"
        else:
            self.handle()



Main().run()
