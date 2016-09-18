from PyQt4 import QtGui,QtCore
import sys
import ui_main
import numpy as np
import pyqtgraph
import SWHear

class ExampleApp(QtGui.QMainWindow, ui_main.Ui_MainWindow):
    def __init__(self, parent=None):
        pyqtgraph.setConfigOption('background', 'w') #before loading widget
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)
        self.grFFT.plotItem.showGrid(True, True, 0.7)
        self.grPCM.plotItem.showGrid(True, True, 0.7)
        self.maxFFT=0
        self.maxPCM=0
        #For mac users, you have to determine what your output audio device is.
        #To do this, first download and install soundflower
        #then, go to your system preferences, audio, and then select soundflower
        #as your output audio. Finally, run python device_info.py in the terminal,
        #and determine which index is soundflower (2ch). From there, set the value of device
        #equal to the index.
        self.ear = SWHear.SWHear(device=2)
        self.ear.stream_start()

    def update(self):
        if not self.ear.data is None and not self.ear.fft is None:
            pcmMax=np.max(np.abs(self.ear.data))
            if pcmMax>self.maxPCM:
                self.maxPCM=pcmMax
                self.grPCM.plotItem.setRange(yRange=[-pcmMax,pcmMax])
            if np.max(self.ear.fft)>self.maxFFT:
                self.maxFFT=np.max(np.abs(self.ear.fft))
                self.grFFT.plotItem.setRange(yRange=[0,self.maxFFT])
            self.pbLevel.setValue(1000*pcmMax/self.maxPCM)
            pen=pyqtgraph.mkPen(color='b')
            self.grPCM.plot(self.ear.datax,self.ear.data,
                            pen=pen,clear=True)
            pen=pyqtgraph.mkPen(color='r')
            self.grFFT.plot(self.ear.fftx[:500],self.ear.fft[:500],
                            pen=pen,clear=True)
        QtCore.QTimer.singleShot(1, self.update) # QUICKLY repeat

if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    form.update() #start with something
    app.exec_()
    print("DONE")
