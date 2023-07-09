import json

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit, QRadioButton, QPushButton, \
    QTextEdit, QFileDialog, QCheckBox, QHBoxLayout, QGridLayout
from PyQt6.QtGui import QClipboard, QPixmap, QCursor
from PyQt6.QtCore import Qt
import os


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle('Gauntlet Data Generator')
        self.resize(700, 600)

        layout = QVBoxLayout()

        # Display Name field
        self.display_name = QLineEdit()
        layout.addWidget(QLabel('Display Name'))
        layout.addWidget(self.display_name)

        # Block Type dropdown
        self.block_type = QComboBox()
        self.block_type.addItems(['Solid (NoteBlocks and Mushroom Blocks)',
                                  'Solid No Culling (Leaf Blocks)',
                                  'No Collision (Redstone, String)',
                                  'Waterlogged (Glow Lichen, String)',
                                  'Waterlogged Solid (Leaves Waterlogged)'])
        layout.addWidget(QLabel('Block Type'))
        layout.addWidget(self.block_type)

        # Placement Rotation dropdown
        self.placement_rotation = QComboBox()
        self.placement_rotation.addItems(['None', 'XZ', 'XZMirror', 'XYZ', 'XYZMirror'])
        self.placement_rotation.currentTextChanged.connect(self.check_rotation)
        layout.addWidget(QLabel('Placement Rotation'))
        layout.addWidget(self.placement_rotation)

        # Random Rotation checkbox
        self.random_rotation = QCheckBox('Random Rotation 0/90/180/270 (Lily Pads)')
        layout.addWidget(QLabel('Random Rotation'))
        layout.addWidget(self.random_rotation)

        # Model Base dropdown
        self.model_bases = {
            'cube': ['down', 'east', 'north', 'south', 'up', 'west'],
            'cube_directional': ['down', 'up', 'north', 'east', 'south', 'west'],
            'cube_all': ['all'],
            'cube_mirrored_all': ['all'],
            'cube_column': ['top', 'side'],
            'cube_bottom_top': ['top', 'bottom', 'side'],
            'orientable': ['front', 'side', 'top']
        }
        self.model_base = QComboBox()
        self.model_base.addItems(self.model_bases.keys())
        layout.addWidget(QLabel('Model Base'))
        layout.addWidget(self.model_base)

        # Texture file fields and previews
        layout.addWidget(QLabel('Texture Files'))
        self.texture_grid = QGridLayout()
        layout.addLayout(self.texture_grid)

        self.ok_button = QPushButton('OK')
        self.ok_button.clicked.connect(self.generate_data)
        layout.addWidget(self.ok_button)

        # Output field and clipboard button
        self.output = QTextEdit()
        self.clipboard_button = QPushButton('Copy to Clipboard')
        self.clipboard_button.clicked.connect(self.copy_to_clipboard)
        layout.addWidget(QLabel('Output'))
        layout.addWidget(self.output)
        layout.addWidget(self.clipboard_button)

        self.setLayout(layout)

        self.model_base.currentTextChanged.connect(self.update_texture_inputs)
        self.model_base.setCurrentText('cube')  # Initialize with 'cube'
        self.update_texture_inputs('cube')

    def browse_texture(self, index):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open file', '', 'Image files (*.png)')
        if filename:
            relative_path = os.path.relpath(filename)
            self.texture_fields[index].setText(relative_path)
            pixmap = QPixmap(filename)
            scaled_pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.FastTransformation)
            self.texture_previews[index].setPixmap(scaled_pixmap)

    def update_texture_inputs(self, model_base):
        # Clear existing widgets
        for i in reversed(range(self.texture_grid.count())):
            widget = self.texture_grid.itemAt(i).widget()
            self.texture_grid.removeWidget(widget)
            widget.setParent(None)

        self.texture_fields = []
        self.texture_previews = []
        for i, texture in enumerate(self.model_bases[model_base]):
            row = i // 3
            col = i % 3

            # Texture label
            label = QLabel(f'{texture.capitalize()} Texture File')
            self.texture_grid.addWidget(label, row * 3, col)

            # Texture preview
            preview = QLabel()
            preview.setFixedSize(100, 100)  # Increase the size of the QLabel
            pixmap = QPixmap(f"{texture}.png")
            scaled_pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.FastTransformation)
            preview.setPixmap(scaled_pixmap)
            preview.mousePressEvent = lambda _, index=i: self.browse_texture(index)
            self.texture_previews.append(preview)
            self.texture_grid.addWidget(preview, row * 3 + 1, col)

            # Texture field
            field = QLineEdit()
            self.texture_fields.append(field)
            self.texture_grid.addWidget(field, row * 3 + 2, col)

    def copy_to_clipboard(self):
        QApplication.clipboard().setText(self.output.toPlainText())

    def check_rotation(self, text):
        if text == "None":
            self.random_rotation.setEnabled(True)
        else:
            self.random_rotation.setEnabled(False)
            self.random_rotation.setChecked(False)

    def generate_data(self):
        # Read current customblocks.json
        with open('customblocks.json') as f:
            data = json.load(f)

        # Get the next index
        last_key = list(data.keys())[-1]
        next_index = data[last_key]['index'] + 1

        # Prepare the new block data
        block_name = self.display_name.text()
        new_block_data = {block_name: {"index": next_index}}

        # Add rotation data if needed
        rotation = self.placement_rotation.currentText()
        if rotation in ['XZ', 'XZMirror', 'XYZ', 'XYZMirror'] and self.model_base.currentText() == 'cube_column':
            new_block_data[block_name]['directions'] = {
                "WEST": next_index + 1,
                "EAST": next_index + 1,
                "NORTH": next_index + 2,
                "SOUTH": next_index + 2,
                "UP": next_index,
                "DOWN": next_index
            }
            next_index += 2  # Increment the index for the next block

        # Get the start index for the note_block.json data
        START_INDEX = next_index

        # Generate the note_block.json data
        INSTRUMENTS = [
            "harp",
            "basedrum",
            "snare",
            "hat",
            "bass",
            "flute",
            "bell",
            "guitar",
            "chime",
            "xylophone",
            "iron_xylophone",
            "cow_bell",
            "didgeridoo",
            "bit",
            "banjo",
            "pling",
            "zombie",
            "skeleton",
            "creeper",
            "dragon",
            "wither_skeleton",
            "piglin",
            "custom_head",
        ]
        note_block_data = {}
        index = START_INDEX
        for _ in range(len(self.texture_fields)):
            for j in range(25):
                for powered in [False, True]:
                    instrument = INSTRUMENTS[index // 50]
                    state = f'instrument={instrument.lower()},note={j},powered={str(powered).lower()}'
                    note_block_data[state] = {"model": f"gauntlet:block/{texture_name}"}
                    index += 1

        # Update the output field
        self.output.setText(json.dumps(note_block_data, indent=4))


app = QApplication([])
window = MainWindow()
window.show()
app.exec()
