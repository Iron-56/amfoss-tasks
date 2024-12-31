from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
import sys
import requests


class PopupWindow(QWidget):
	def __init__(self, pixmap, data):
		super().__init__()

		self.popup_window = None

		self.setWindowTitle(" ")
		self.setFixedSize(360, 480)

		self.setStyleSheet("""
			

			QWidget {
				background-color: dark-grey;
			}
			
			QLabel {
				font-size: 16px;
				background-color: dark-grey;
				color: white;
				border: 2px solid #BA263E;
				border-radius: 10px;
				padding: 1px;
				margin: 6px;
			}
		""")

		layout = QVBoxLayout(self)

		w = h = 225
		image = QLabel(self)
		image.setPixmap(pixmap)
		image.setFixedSize(w, h)
		image.setScaledContents(True)
		image.setAlignment(Qt.AlignCenter)
		image.setStyleSheet("border: 0px; background-color: grey;")

		layout.addWidget(image, alignment=Qt.AlignCenter)

		grid_layout = QGridLayout()

		attack = QLabel(f"Attack: {data[4]['base_stat']}", self)
		attack.setAlignment(Qt.AlignCenter)
		grid_layout.addWidget(attack, 0, 0)

		defense = QLabel(f"Defense: {data[3]['base_stat']}", self)
		defense.setAlignment(Qt.AlignCenter)
		grid_layout.addWidget(defense, 1, 0)

		hp = QLabel(f"HP: {data[5]['base_stat']}", self)
		hp.setAlignment(Qt.AlignCenter)
		grid_layout.addWidget(hp, 2, 0)

		speed = QLabel(f"Speed: {data[0]['base_stat']}", self)
		speed.setAlignment(Qt.AlignCenter)
		grid_layout.addWidget(speed, 0, 1)

		sp_atk = QLabel(f"Special Attack: {data[2]['base_stat']}", self)
		sp_atk.setAlignment(Qt.AlignCenter)
		grid_layout.addWidget(sp_atk, 1, 1)

		sp_def = QLabel(f"Special Defense: {data[1]['base_stat']}", self)
		sp_def.setAlignment(Qt.AlignCenter)
		grid_layout.addWidget(sp_def, 2, 1)

		layout.addLayout(grid_layout)



if __name__ == "__main__":
	app = QApplication(sys.argv)
	data = eval(open("assets/pokemon.json", "r").read())
	for pokemon in data['results']:
		if pokemon['name'] == "pikachu":
			poke = requests.get(pokemon['url']).json()
			pixmap = QPixmap()
			pixmap.loadFromData(requests.get(poke['sprites']['other']['official-artwork']['front_default']).content)
			window = PopupWindow(pixmap, poke['stats'])
			window.show()
			break
	sys.exit(app.exec())