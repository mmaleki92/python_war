import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon


class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.statusBar()

        # Create File menu
        fileMenu = self.menuBar().addMenu('File')

        # Create Open action
        openAction = QAction(QIcon(), 'Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open file')
        openAction.triggered.connect(self.openFile)
        fileMenu.addAction(openAction)

        # Create Save action
        saveAction = QAction(QIcon(), 'Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save file')
        saveAction.triggered.connect(self.saveFile)
        fileMenu.addAction(saveAction)

        # Create Exit action
        exitAction = QAction(QIcon(), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)

        self.setGeometry(300, 300, 600, 450)
        self.setWindowTitle('Text Editor')
        self.show()

    def openFile(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open File')
        if filename:
            with open(filename, 'r') as file:
                self.textEdit.setText(file.read())

    def saveFile(self):
        filename, _ = QFileDialog.getSaveFileName(self, 'Save File')
        if filename:
            with open(filename, 'w') as file:
                file.write(self.textEdit.toPlainText())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     'Are you sure you want to quit?',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = TextEditor()
    sys.exit(app.exec_())
