from PyQt5.QtWidgets import QWidget, QLabel, \
    QLineEdit, QGridLayout, QPushButton


class Menu(QWidget):
    def __init__(self, observer, func_for_click):
        super().__init__()
        self.observer = observer
        self.func_for_click = func_for_click
        self.initUI()

    def initUI(self):
        latitude = QLabel('Latitude')
        longitude = QLabel('Longitude')
        angle_of_observe = QLabel('Angle')
        vector_of_watch = QLabel('Vector')
        time = QLabel('Time')
        self.latitudeEdit = QLineEdit(str(self.observer.input_latitude))
        self.longitudeEdit = QLineEdit(str(self.observer.input_longitude))
        self.angle_of_observeEdit = QLineEdit(str(self.observer.input_angle))
        self.timeEdit = QLineEdit(self.observer.input_time_now)
        self.vector_of_watchEdit = QLineEdit(self.observer.input_vector)
        editButton = QPushButton('Edit')
        grid = QGridLayout()
        grid.setSpacing(0)
        grid.addWidget(latitude, 0, 0)
        grid.addWidget(self.latitudeEdit, 0, 2)
        grid.addWidget(longitude, 1, 0)
        grid.addWidget(self.longitudeEdit, 1, 2)
        grid.addWidget(angle_of_observe, 2, 0)
        grid.addWidget(self.angle_of_observeEdit, 2, 2)
        grid.addWidget(vector_of_watch, 3, 0)
        grid.addWidget(self.vector_of_watchEdit, 3, 2)
        grid.addWidget(time, 4, 0)
        grid.addWidget(self.timeEdit, 4, 2)
        grid.addWidget(editButton, 5, 2)
        editButton.clicked.connect(self.func_for_click)
        self.setLayout(grid)
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('SkyMenu')
