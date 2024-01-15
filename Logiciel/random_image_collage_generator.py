import os
import random
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy, QFileDialog, QTextBrowser, QTextEdit
from PyQt5.QtGui import QPixmap, QTextDocument, QKeyEvent
from PyQt5.QtCore import Qt
from PIL import Image

class RandomImageCollageGenerator(QWidget):
    def __init__(self):

        super(RandomImageCollageGenerator, self).__init__()

        self.folder_path = "Frames"
        self.texts_path = "Texts"
        self.selected_folder = ""

        self.layout = QVBoxLayout(self)

        self.setup_ui()

    def setup_ui(self):
        self.setGeometry(100, 100, 1920, 1080)
        generate_button = QPushButton("Générer le collage", self)
        generate_button.clicked.connect(self.generate_collage)
        self.layout.addWidget(generate_button)

        content_layout = QHBoxLayout()

        self.canvas = QLabel(self)
        content_layout.addWidget(self.canvas)

        self.text_layout = QVBoxLayout()

        self.text_browser = QTextBrowser(self)
        self.text_browser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.text_layout.addWidget(self.text_browser)

        self.note_label = QLabel("Cliquez sur l'image pour révéler la solution", self)
        self.note_label.setAlignment(Qt.AlignCenter)
        self.text_layout.addWidget(self.note_label)

        self.text_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.addLayout(self.text_layout)

        self.layout.addLayout(content_layout)

        self.text_browser.setHidden(True)
        self.note_label.setHidden(True)

        self.canvas.mousePressEvent = self.on_canvas_click

    def on_key_press_event(self, event: QKeyEvent):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.text_browser.setHidden(True)
            self.generate_collage()
        else:
            self.text_browser.setHidden(True)
            super().keyPressEvent(event)
    
    def on_canvas_click(self, event):
        if self.text_browser.isHidden():
            self.text_browser.setHidden(False)
            self.note_label.setHidden(True)
        else:
            self.text_browser.setHidden(True)
            self.note_label.setHidden(False)

    def select_random_folder(self):
        folders = [f for f in os.listdir(self.folder_path) if os.path.isdir(os.path.join(self.folder_path, f))]
        if folders:
            self.selected_folder = os.path.join(self.folder_path, random.choice(folders))
            print(f"Dossier sélectionné: {self.selected_folder}")
        else:
            print("Aucun dossier trouvé.")

    def get_text_from_file(self):
        text_file_path = os.path.join(self.texts_path, f"{os.path.basename(self.selected_folder)}.txt")
        if os.path.exists(text_file_path):
            with open(text_file_path, 'r', encoding='utf-8') as file:
                return file.read()
        else:
            return "Aucun texte trouvé."

    def apply_tags(self):
        # Si besoin d'ajuster le texte, les balises, etc., faites-le ici
        pass


    # Remplacez cette partie dans votre script existant

    def generate_collage(self):
        self.select_random_folder()
        self.text_browser.setHidden(True)
        if self.selected_folder:
            image_files = [f for f in os.listdir(self.selected_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

            if len(image_files) >= 4:
                images = []

                random.shuffle(image_files)
                selected_images = image_files[:4]

                # Fixez la largeur du collage (ajustez selon vos besoins)
                collage_width = 700

                # Fixez le nombre de colonnes
                columns = 2

                for i, image_file in enumerate(selected_images):
                    image_path = os.path.join(self.selected_folder, image_file)
                    img = Image.open(image_path)

                    # Redimensionnez en conservant la proportion d'origine
                    new_size = (collage_width // columns, int((collage_width // columns / img.width) * img.height))
                    img = img.resize(new_size, Image.LANCZOS)

                    images.append(img)

                # Calcul de la hauteur totale nécessaire pour le collage
                rows = len(images) // columns
                if len(images) % columns != 0:
                    rows += 1
                collage_height = sum(images[i].height for i in range(0, len(images), columns))

                collage = Image.new('RGB', (collage_width, collage_height))

                current_height = 0
                for i in range(0, len(images), columns):
                    for j in range(columns):
                        if i + j < len(images):
                            collage.paste(images[i + j], (j * (collage_width // columns), current_height))
                    current_height += images[i].height

                self.text_browser.setHtml(f"<center>{self.get_text_from_file()}</center>")
                self.note_label.setHidden(False)
                self.display_collage(collage)
            else:
                print("Le dossier ne contient pas assez d'images (au moins 4).")
        else:
            print("Aucun dossier sélectionné.")

    def display_collage(self, collage):
        image_path = "temp_collage.png"
        collage.save(image_path)

        pixmap = QPixmap(image_path)
        self.canvas.setPixmap(pixmap)

        os.remove(image_path)



