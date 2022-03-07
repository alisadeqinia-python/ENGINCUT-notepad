from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from PyQt5 import uic
from Images import image_rc

class MyGUI(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MyGUI, self).__init__(*args, **kwargs)
        uic.loadUi('notepad.ui', self)
        self.show()

        # setting font to the editor
        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(12)
        self.plainTextEdit.setFont(fixedfont)

        #if it's None, we have no file opened and not saved file
        self.path = None

        #Set title
        self.setWindowTitle("ENGINCUT Notepad")

        #Triggers
        self.actionArial.triggered.connect(lambda: self.change_font("Arial"))
        self.actionCambria.triggered.connect(lambda: self.change_font("Cambria"))
        self.actionCalibari.triggered.connect(lambda: self.change_font("Calibri"))
        self.action12.triggered.connect(lambda: self.change_font_size(12))
        self.action14.triggered.connect(lambda: self.change_font_size(14))
        self.action24.triggered.connect(lambda: self.change_font_size(24))
        self.actionNew.triggered.connect(self.file_new)
        self.actionPrint.triggered.connect(self.file_print)
        self.actionOpen.triggered.connect(self.open_file)
        self.actionSave.triggered.connect(self.file_save)
        self.actionSave_as.triggered.connect(self.file_saveas)
        self.actionWrap_Text.triggered.connect(self.edit_toggle_wrap)

    def change_font(self, font_name):
        self.plainTextEdit.setFont(QFont(font_name, 12))

    def change_font_size(self, size):
        self.plainTextEdit.setFont(QFont("Arial", size))

    def file_new(self):
        if self.path is None:
            self.file_saveas()
        self.plainTextEdit.clear()
        self.setWindowTitle("Untitled- ENGINCUT Notepad")
        self.path = None

    def file_print(self):
        # creating a QPrintDialog
        printobj = QPrintDialog()
        # if executed
        if printobj.exec_():
        # print the text
            self.plainTextEdit.print_(printobj.printer())

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self,"Open File","", "Text Files (*.txt);;Python Files(*.py)")
        if path:
            try:
                with open(path,"r") as f:
                    text=f.read()
            except Exception as e:
                self.dialog_critical(str(e))
            else:
                self.path=path
                self.plainTextEdit.setPlainText(text)

    def file_save(self):
        if self.path is None:
            return self.file_saveas()
        self._save_to_path(self.path)

    def file_saveas(self):
        # opening path
        path, _ = QFileDialog.getSaveFileName(self,"Save file","",
                                              "Text documents (*.txt);;All files (*.*)")

        # if dialog is cancelled i.e no path is selected
        if not path:
            # return this method
            # i.e no action performed
            return
        # else call save to path method
        self._save_to_path(path)

    def _save_to_path(self, path):
        # get the text
        text = self.plainTextEdit.toPlainText()
        # try catch block
        try:
           # opening file to write
            with open(path,'w') as f:
                # write text in the file
                f.write(text)
        # if error occurs
        except Exception as e:

            # show error using critical
            self.dialog_critical(str(e))

        # else do this
        else:
            # change path
            self.path = path
            # update the title
            self.update_title()

    def update_title(self):
        # setting window title with prefix as file name
        # suffix aas PyQt5 Notepad
        self.setWindowTitle("%s - ENGINCUT Notepad" % (os.path.basename(self.path)
                                                    if self.path else "Untitled"))

    def dialog_critical(self, s):
        # creating a QMessageBox object
        dlg = QMessageBox(self)
        # setting text to the dlg
        dlg.setText(s)
        # setting icon to it
        dlg.setIcon(QMessageBox.Critical)
        # showing it
        dlg.show()

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(self,"Save File","", "Text Files (*.txt);Python Files(*.py)")
        text = self.plainTextEdit.toPlaneText(self)
        if filename != "":
            with open(filename,"w") as f:
                f.write(text)

    def edit_toggle_wrap(self):
        # chaining line wrap mode
        self.plainTextEdit.setLineWrapMode(1 if self.plainTextEdit.lineWrapMode() == 0 else 0 )


def main():
    app = QApplication([])
    window = MyGUI()
    app.exec_()


if __name__ == '__main__':
    main()
