from ledscreen import *

class AlphaComponent():
    def compute(self):
        pass

    def display(self, screen, data):
        pass

class TimeAlphaComponent(AlphaComponent):
    def compute(self):
        pass
    def display(self, screen, data):
        #components.AdaptativeTextComponent('Hello everybody!', 0, 0, 32, 8)
        pass

class ComponentManager():

    componentList = []

    def load(self):
        with open('./conf/components.conf') as f:
            lines = f.readlines()
        for line in lines:
            c = eval(line)
            self.componentList.append(c)
