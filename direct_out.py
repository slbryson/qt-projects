import logging
import sys
try:
    import configparser
except:
    from configparser import SafeConfigParser

from configupdater import ConfigUpdater

import os

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
from PyQt5.QtWidgets import QGridLayout, QFrame

from PyQt5 import QtGui, QtCore


if sys.version_info < (3,):
    import ConfigParser as configparser
    unicode = str
else:
    import configparser
    unicode = str
#from PyQt5 import QtWidgets as qt_widgets


logger = logging.getLogger(__name__)

def ConfigSectionMap(section):
    dict1 = {}
    Config = configparser.ConfigParser()
    Config.read("./config.ini")
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1
def save_config():
        config = configparser.ConfigParser(allow_no_value=True)
        config.read("./config.ini")

        updater = ConfigUpdater()
        try:
            updater.read_file('config.ini')
        except Exception as rt_err:
            raise rt_err


        # config.set('Configuration', 'locale', self.config['locale'])
        # config.set('Configuration', 'font-size', self.config['font-size'])
        # Try New format all together
        for section_name in updater.sections():
            print(section_name)

            
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
        frameStyle = QFrame.Sunken | QFrame.Panel

        # setup the ui
        self.setGeometry(200, 100, 800, 500)
        self.setWindowTitle('Bryson Input GUI')
        #Console
        #self._console = QTextBrowser(self)
        self._console = QTextEdit(self)
        self._console.move(300, 75)
        self._console.resize(200,200)

        #Button
        self._button  = QPushButton(self)
        self._button.move(40,400)
        self._button.setText('Test Me')
        self._button.clicked.connect(self.test)

        # Add another Button to load config.ini data
        self._dbButton = QPushButton(self)
        self._dbButton.move(40,200)
        self._dbButton.setText('DB File')
        #output = get_string()
        self._dbButton.clicked.connect(self.write_config)

        # Create a label next to the button
        self.label ={}
        self.setStyleSheet("""QToolTip {
                           color: black;
                           }
                           QLabel{
                           background-color: white;
                           }
                        #    QPushButton {
                        #    font-weight: bold;
                           }""")
        self.label['dailyPCP'] = QTextEdit(self)
        self.label['dailyPCP'].move(180,200)
        output = self.read_dbmaster()
        self.label['dailyPCP'].setText(output)
        #self.label['dailyPCP'].setFrameStyle(frameStyle)
       
        # create the layout
        #layout = QGridLayout()
        layout = QVBoxLayout()
        layout.addWidget(self._console)
        layout.addWidget(self._button)
        layout.addWidget(self._dbButton)
        layout.addWidget(self.label['dailyPCP'])



        openFile = QAction('&Open File', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open File')
        openFile.triggered.connect(self.file_open)

        # create connections
        #self.python_version_label = qt_widgets.QLabel()

        XStream.stdout().messageWritten.connect( self._console.insertPlainText )
        XStream.stderr().messageWritten.connect( self._console.insertPlainText )

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(openFile)

        self.home()
        self.show()
        self.raise_()

 

    def home(self):
        btn = QPushButton('Quit', self)
        btn.clicked.connect(self.close_application)
        btn.resize(btn.sizeHint())
        btn.move(10, 465)

    def read_dbmaster(self):
    #   Add somewhere
        config = configparser.ConfigParser()
        file_handler = ConfigSectionMap('main')
        #The only thing that the user might specify is a filetype to limit on
        master_file = file_handler['master']
        self.label['dailyPCP'].setText("{}".format(master_file))
        return master_file

    def write_config(self):
        save_config()
        return


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
