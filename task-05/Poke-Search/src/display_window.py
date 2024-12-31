from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QPushButton
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
import sys, os
import requests

class PokeDisplay(QWidget):
	def __init__(self):
		super().__init__()
		self.display_window = None

		self.setWindowTitle("Captured Pokemons")
		self.setFixedSize(350, 400)
		
		self.setStyleSheet("""
			

			QWidget {
				background-color: dark-grey;
			}
			
			QLabel {
				font-size: 16px;
				color: white;
				border: 2px solid #BA263E;
				border-radius: 10px;
				padding: 1px;
				margin: 6px;
			}
			
			QPushButton {
				color: white;
				border: 1px solid #BA263E;
				font: bold 16px;
				text-align: center;
				border-radius: 10px;
				margin: 6px;
				padding: 6px;
			}
			
			QPushButton:hover {
				background-color: #BA263E;
				color: dark-grey;
			}
		""")

		layout = QVBoxLayout(self)

		self.index = 0
		self.captured = sorted(os.listdir("assets/captured"))
		self.path = "assets/captured/"

		w = h = 280
		self.pixmap = QPixmap(self.path+self.captured[0])
		self.image = QLabel(self)
		self.image.setPixmap(self.pixmap)
		self.image.setFixedSize(w, h)
		self.image.setScaledContents(True)
		self.image.setAlignment(Qt.AlignCenter)
		self.image.setStyleSheet("border: 0px; background-color: grey;")

		layout.addWidget(self.image, alignment=Qt.AlignCenter)

		self.name = QLabel(self.captured[self.index].split(".")[0], self)
		self.name.setStyleSheet("font-size: 24px; border: 0px;")

		layout.addWidget(self.name, alignment=Qt.AlignCenter)

		grid_layout = QGridLayout()

		previous = QPushButton("Previous", self)
		previous.clicked.connect(self.previous_pokemon)
		grid_layout.addWidget(previous, 0, 0)

		next = QPushButton("Next", self)
		next.clicked.connect(self.next_pokemon)
		grid_layout.addWidget(next, 0, 1)

		layout.addLayout(grid_layout)
	
	def update(self):
		self.pixmap.load(self.path+self.captured[self.index])
		self.image.setPixmap(self.pixmap)
		self.name.setText(self.captured[self.index].split(".")[0])
	
	def next_pokemon(self, txt):
		if self.index == len(self.captured)-1:
			self.index = 0
		self.index += 1
		self.update()
	
	def previous_pokemon(self):
		if self.index == 0:
			self.index = len(self.captured)-1
		self.index -= 1
		self.update()

if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = PokeDisplay()
	window.show()
	sys.exit(app.exec())