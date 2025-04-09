from ui.main_window import MainWindow
from models.baggage import Baggage
from PyQt6.QtWidgets import QApplication
import sys


def main():
    baggage = Baggage()

    app = QApplication(sys.argv)
    window = MainWindow(baggage)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
