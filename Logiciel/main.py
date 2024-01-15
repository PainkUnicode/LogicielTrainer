from PyQt5. QtWidgets import QApplication
from random_image_collage_generator import RandomImageCollageGenerator

if __name__ == "__main__":
    app = QApplication([])
    window = RandomImageCollageGenerator()
    window.show()
    app.exec_()
