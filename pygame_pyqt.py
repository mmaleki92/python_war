import sys
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QColor, QTextCharFormat, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.Qsci import QsciScintilla, QsciLexerPython


class SyntaxHighlighter(QsciLexerPython):
    def __init__(self, parent):
        super().__init__(parent)
        self.setDefaultFont(QFont('Courier New', 10))

        self.keyword_format = QTextCharFormat()
        self.keyword_format.setForeground(Qt.darkBlue)
        self.keyword_format.setFontWeight(QFont.Bold)

        keywords = [
            'False', 'None', 'True', 'and', 'as', 'assert', 'break', 'class',
            'continue', 'def', 'del', 'elif', 'else', 'except', 'finally',
            'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda',
            'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while',
            'with', 'yield'
        ]

        self.keyword_format.setFontWeight(QFont.Bold)
        self.keyword_format.setForeground(Qt.darkBlue)

        self.keyword_format.setFontWeight(QFont.Bold)
        self.keyword_format.setForeground(Qt.darkBlue)

        for word in keywords:
            self.setStyling(len(word), self.keyword_format)

    def styleText(self, start, end):
        text = self.editor().text()[start:end]
        expression = QRegExp(r'\b\w+\b')

        index = expression.indexIn(text)
        while index >= 0:
            length = expression.matchedLength()
            self.setStyling(length, self.keyword_format)
            index = expression.indexIn(text, index + length)


class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Python Text Editor')

        self.editor = QsciScintilla()
        self.setCentralWidget(self.editor)

        lexer = SyntaxHighlighter(self.editor)
        self.editor.setLexer(lexer)

        self.setGeometry(100, 100, 800, 600)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = TextEditor()
    sys.exit(app.exec_())
