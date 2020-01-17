from fbs_runtime.application_context.PySide2 import ApplicationContext
import sys
from app import App
from qtapp import MainWindow
from controller import Controller
if __name__ == '__main__':
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    appctxt.app.setStyle('Fusion')
    window = MainWindow(Controller(App(), appctxt))
    window.resize(1800, 1000)
    window.show()
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
    