import logging
import sys

from PyQt5.QtCore import QObject,\
                         pyqtSignal

from PyQt5.QtWidgets import QDialog, \
                        QVBoxLayout, \
                        QPushButton, \
                        QTextBrowser,\
                        QApplication
from PyQt5.QtCore import QCoreApplication,QObject, pyqtSignal, Qt
from PyQt5.QtGui import QIcon, QColor 
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QAction, QMessageBox,QTextBrowser
from PyQt5.QtWidgets import QCalendarWidget, QFontDialog, QColorDialog, QTextEdit, QFileDialog, QDialog, QVBoxLayout
from PyQt5.QtWidgets import QCheckBox, QProgressBar, QComboBox, QLabel, QStyleFactory, QLineEdit, QInputDialog
from PyQt5.QtWidgets import QGridLayout

logger = logging.getLogger(__name__)

class XStream(QObject):
    _stdout = None
    _stderr = None

    messageWritten = pyqtSignal(str)

    def flush( self ):
        pass

    def fileno( self ):
        return -1

    def write( self, msg ):
        if ( not self.signalsBlocked() ):
            self.messageWritten.emit(str(msg))

    @staticmethod
    def stdout():
        if ( not XStream._stdout ):
            XStream._stdout = XStream()
            sys.stdout = XStream._stdout
        return XStream._stdout

    @staticmethod
    def stderr():
        if ( not XStream._stderr ):
            XStream._stderr = XStream()
            sys.stderr = XStream._stderr
        return XStream._stderr

class MyInputWindow(QMainWindow):
    def __init__( self, parent = None ):
        super(MyInputWindow, self).__init__(parent)

        # setup the ui
        self.setGeometry(50, 50, 800, 500)

        self._console = QTextBrowser(self)
        self._console = QTextEdit(self)
        #self._console.move(5, 20)
        self._console.resize(400,200)
        self._button  = QPushButton(self)
        self._button.move(500,100)
        self._button.setText('Test Me')
        
        # create the layout
        layout = QGridLayout()
        layout.addWidget(self._console)
        layout.addWidget(self._button)
        layout.setColumnStretch(2, 5)
        layout.setColumnStretch(1, 0)
        layout.setColumnMinimumWidth(1, 75)
        layout.setColumnMinimumWidth(2, 120)


        openFile = QAction('&Open File', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open File')
        openFile.triggered.connect(self.file_open)

        # create connections
        #self.python_version_label = qt_widgets.QLabel()
        n  = 3
        layout.addWidget(self._console, n, 0, 2, 2)
        XStream.stdout().messageWritten.connect( self._console.insertPlainText )
        XStream.stderr().messageWritten.connect( self._console.insertPlainText )

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(openFile)
        self._button.clicked.connect(self.test)

        self.home()

    def home(self):
        btn = QPushButton('quit', self)
        btn.clicked.connect(self.close_application)
        btn.resize(btn.sizeHint())
        btn.move(0, 100)

    def file_open(self):
        # need to make name an tupple otherwise i had an error and app crashed
        name, _ = QFileDialog.getOpenFileName(self, 'Open File', options=QFileDialog.DontUseNativeDialog)
        print('tot na dialog gelukt')  # for debugging
        file = open(name, 'r')
        print('na het inlezen gelukt') # for debugging
        # self.editor()

        with file:
            text = file.read()
            # self.textEdit.setText(text)
            self._console.setText(text)

    def test( self ):
        # print some stuff
        print('testing')
        print('testing2')

        # log some stuff
        logger.debug('Testing debug')
        logger.info('Testing info')
        # logger.warning('Testing warning')
        # logger.error('Testing error')

        # error out something
        #print(intended_to_capture_error_on_screen)
    def close_application(self):

        choice = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if choice == QMessageBox.Yes:
            print('quit application')
            sys.exit()
        else:
            pass

if ( __name__ == '__main__' ):
    logging.basicConfig()

    app = None
    if ( not QApplication.instance() ):
        app = QApplication([])

    dlg = MyInputWindow()
    dlg.show()

    if ( app ):
        app.exec_()