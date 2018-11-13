from Model.Parser import Parser
from View.View import View


class Controller:

    def __init__(self):
        self.root = ()
        self.view = View(self.root)

    def start(self):
        print('start')
