import json
import sys
import webbrowser
from pathlib import Path

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction, QFont
from PySide6.QtWidgets import (
    QApplication, QComboBox, QDialog, QFormLayout, QHBoxLayout, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QMainWindow, QMessageBox,
    QPushButton, QScrollArea, QSplitter, QVBoxLayout, QWidget
)

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"


def load_json(name):
    with open(DATA / name, "r", encoding="utf-8") as f:
        return json.load(f)


class DorkDialog(QDialog):
    def __init__(self, parent, templates):
        super().__init__(parent)
        self.setWindowTitle("OSINT-Recall • Dork Generator")
        self.setMinimumWidth(650)
        self.templates = templates
        layout = QVBoxLayout(self)

        row = QHBoxLayout()
        row.addWidget(QLabel("Template"))
        self.combo = QComboBox()
        self.combo.addItems([x["name"] for x in templates])
        row.addWidget(self.combo, 1)
        layout.addLayout(row)

        self.form = QFormLayout()
        layout.addLayout(self.form)

        self.result = QLineEdit()
        self.result.setReadOnly(True)
        layout.addWidget(QLabel("Generated query"))
        layout.addWidget(self.result)

        buttons = QHBoxLayout()
        generate = QPushButton("Generate")
        copy = QPushButton("Copy")
        buttons.addStretch()
        buttons.addWidget(generate)
        buttons.addWidget(copy)
        layout.addLayout(buttons)

        generate.clicked.connect(self.generate)
        copy.clicked.connect(self.copy_result)
        self.combo.currentIndexChanged.connect(self.build_form)
        self.build_form(0)

    def build_form(self, index):
        while self.form.rowCount():
            self.form.removeRow(0)
        self.inputs = {}
        item = self.templates[index]
        for field in item["fields"]:
            edit = QLineEdit()
            edit.setPlaceholderText(field.get("placeholder", ""))
            self.inputs[field["name"]] = edit
            self.form.addRow(field["label"], edit)
        self.result.setText(item.get("example", ""))

    def generate(self):
        item = self.templates[self.combo.currentIndex()]
        values = {k: v.text().strip() for k, v in self.inputs.items()}
        if any(not value for value in values.values()):
            QMessageBox.warning(self, "Missing field", "Fill in all fields first.")
            return
        query = item["template"]
        for key, value in values.items():
            query = query.replace("{" + key + "}", value)
        self.result.setText(query)

    def copy_result(self):
        if self.result.text():
            QApplication.clipboard().setText(self.result.text())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.techniques = load_json("techniques.json")
        self.dorks = load_json("dorks.json")
        self.tools = load_json("tools.json")
        self.filtered = []
        self.setWindowTitle("OSINT-Recall")
        self.resize(1180, 720)
        self.setMinimumSize(900, 600)
        self.build_menu()
        self.build_ui()
        self.apply_theme()
        self.refresh_results()

    def build_menu(self):
        tools_menu = self.menuBar().addMenu("Tools")
        dork_action = QAction("Dork Generator", self)
        dork_action.triggered.connect(self.open_dork_generator)
        tools_menu.addAction(dork_action)

        resources = self.menuBar().addMenu("Public Resources")
        for tool in self.tools:
            action = QAction(tool["name"], self)
            action.triggered.connect(
                lambda checked=False, url=tool["url"]: webbrowser.open(url)
            )
            resources.addAction(action)

    def build_ui(self):
        root = QWidget()
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(18, 16, 18, 16)
        root_layout.setSpacing(12)

        header = QHBoxLayout()
        title_box = QVBoxLayout()
        title = QLabel("OSINT-RECALL")
        title.setObjectName("Title")
        subtitle = QLabel("Search  •  Learn  •  Recall  •  Generate")
        subtitle.setObjectName("Subtitle")
        title_box.addWidget(title)
        title_box.addWidget(subtitle)
        header.addLayout(title_box)
        header.addStretch()

        self.count_label = QLabel()
        self.count_label.setObjectName("Count")
        header.addWidget(self.count_label)
        root_layout.addLayout(header)

        search_row = QHBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search techniques, tags, categories...")
        self.search.setClearButtonEnabled(True)
        self.search.textChanged.connect(self.refresh_results)
        search_row.addWidget(self.search, 1)

        self.category = QComboBox()
        self.category.addItem("All categories")
        for category in sorted({x["category"] for x in self.techniques}):
            self.category.addItem(category)
        self.category.currentTextChanged.connect(self.refresh_results)
        search_row.addWidget(self.category)
        root_layout.addLayout(search_row)

        splitter = QSplitter(Qt.Horizontal)

        self.list = QListWidget()
        self.list.setMinimumWidth(330)
        self.list.setSpacing(4)
        self.list.currentRowChanged.connect(self.show_selected)
        splitter.addWidget(self.list)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.detail = QWidget()
        self.detail_layout = QVBoxLayout(self.detail)
        self.detail_layout.setContentsMargins(22, 8, 22, 18)
        scroll.setWidget(self.detail)
        splitter.addWidget(scroll)
        splitter.setSizes([370, 760])
        root_layout.addWidget(splitter, 1)

        bottom = QHBoxLayout()
        bottom.addStretch()
        dork = QPushButton("⚡ Dork Generator")
        dork.clicked.connect(self.open_dork_generator)
        bottom.addWidget(dork)
        root_layout.addLayout(bottom)

        self.setCentralWidget(root)

    def refresh_results(self):
        query = self.search.text().lower().strip()
        category = self.category.currentText()

        self.filtered = [
            item for item in self.techniques
            if (category == "All categories" or item["category"] == category)
            and (
                not query
                or query in json.dumps(item, ensure_ascii=False).lower()
            )
        ]

        self.list.blockSignals(True)
        self.list.clear()
        for item in self.filtered:
            row = QListWidgetItem(f'{item["title"]}\n{item["category"]}')
            row.setSizeHint(QSize(0, 58))
            self.list.addItem(row)
        self.list.blockSignals(False)

        self.count_label.setText(f"{len(self.filtered)} techniques")
        if self.filtered:
            self.list.setCurrentRow(0)
        else:
            self.show_empty()

    def clear_detail(self):
        while self.detail_layout.count():
            item = self.detail_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def show_empty(self):
        self.clear_detail()
        label = QLabel("No technique found")
        label.setObjectName("Empty")
        self.detail_layout.addWidget(label)
        self.detail_layout.addStretch()

    def show_selected(self, row):
        if row < 0 or row >= len(self.filtered):
            return

        self.clear_detail()
        item = self.filtered[row]

        badge = QLabel(item["category"].upper())
        badge.setObjectName("Badge")
        self.detail_layout.addWidget(badge)

        title = QLabel(item["title"])
        title.setObjectName("DetailTitle")
        title.setWordWrap(True)
        self.detail_layout.addWidget(title)

        summary = QLabel(item["summary"])
        summary.setObjectName("Summary")
        summary.setWordWrap(True)
        self.detail_layout.addWidget(summary)

        self.add_section("LEARN", item["learn"])
        self.add_section(
            "EXAMPLES",
            "\n".join(f"• {example}" for example in item["examples"])
        )
        self.add_section("NOTES", item["notes"])

        tags = QLabel("   ".join(f"#{tag}" for tag in item.get("tags", [])))
        tags.setObjectName("Tags")
        tags.setWordWrap(True)
        self.detail_layout.addWidget(tags)
        self.detail_layout.addStretch()

    def add_section(self, heading, text):
        label = QLabel(heading)
        label.setObjectName("Section")
        self.detail_layout.addWidget(label)

        body = QLabel(text)
        body.setWordWrap(True)
        body.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.detail_layout.addWidget(body)

    def open_dork_generator(self):
        DorkDialog(self, self.dorks).exec()

    def apply_theme(self):
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background: #101318;
                color: #e8edf2;
            }
            QLineEdit, QComboBox {
                background: #181d24;
                border: 1px solid #303844;
                border-radius: 8px;
                padding: 9px;
                color: #e8edf2;
            }
            QListWidget {
                background: #141920;
                border: 1px solid #303844;
                border-radius: 10px;
                padding: 6px;
            }
            QListWidget::item {
                padding: 8px;
                border-radius: 7px;
                color: #c8d0da;
            }
            QListWidget::item:selected {
                background: #26364a;
                color: white;
            }
            QPushButton {
                background: #243449;
                border: 1px solid #3b5069;
                border-radius: 8px;
                padding: 9px 14px;
            }
            QPushButton:hover {
                background: #30455e;
            }
            QSplitter::handle {
                background: #242b34;
            }
            #Title {
                font-size: 25px;
                font-weight: 800;
            }
            #Subtitle {
                color: #7f8b99;
            }
            #Count {
                color: #8295aa;
            }
            #Badge {
                color: #86b9ff;
                font-size: 11px;
                font-weight: 700;
                padding: 4px 0;
            }
            #DetailTitle {
                font-size: 30px;
                font-weight: 800;
            }
            #Summary {
                color: #aeb8c4;
                font-size: 14px;
            }
            #Section {
                color: #7fb2f5;
                font-weight: 800;
                margin-top: 14px;
            }
            #Tags {
                color: #718096;
                margin-top: 18px;
            }
            #Empty {
                color: #748091;
                font-size: 18px;
            }
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("OSINT-Recall")
    app.setFont(QFont("Segoe UI", 10))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
