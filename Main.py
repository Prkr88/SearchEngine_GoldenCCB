from Controller.Controller import Controller
from Model.ReadFile import ReadFile

from View.GoldenUI import Gu
from PyQt5 import QtWidgets

if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = Gu('resources//GoldenUIv2.ui')
    window.setup_ui()
    window.show()
    sys.exit(app.exec_())


