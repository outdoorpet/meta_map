from PyQt4 import QtCore, QtGui, QtWebKit, QtNetwork
from obspy import read_inventory
import functools
import os
from query_input_yes_no import query_yes_no
import sys


class MainWindow(QtGui.QWidget):
    """
    Main Window for metadata map GUI
    """

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi()
        self.show()
        self.raise_()

    def setupUi(self):
        vbox = QtGui.QVBoxLayout()
        self.setLayout(vbox)

        hbox = QtGui.QHBoxLayout()
        open_xml_button = QtGui.QPushButton('Open StationXML')
        openXml = functools.partial(self.open_xml_file)
        open_xml_button.released.connect(openXml)
        hbox.addWidget(open_xml_button)

        vbox.addLayout(hbox)

        view = self.view = QtWebKit.QWebView()
        cache = QtNetwork.QNetworkDiskCache()
        cache.setCacheDirectory("cache")
        view.page().networkAccessManager().setCache(cache)
        view.page().networkAccessManager()

        view.page().mainFrame().addToJavaScriptWindowObject("MainWindow", self)
        view.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        view.load(QtCore.QUrl('map.html'))
        view.loadFinished.connect(self.onLoadFinished)
        view.linkClicked.connect(QtGui.QDesktopServices.openUrl)

        vbox.addWidget(view)

    def onLoadFinished(self):
        with open('map.js', 'r') as f:
            frame = self.view.page().mainFrame()
            frame.evaluateJavaScript(f.read())

    def open_xml_file(self):
        self.filename = str(QtGui.QFileDialog.getOpenFileName(
            parent=self, caption="Choose File",
            directory=os.path.expanduser("~"),
            filter="XML Files (*.xml)"))
        if not self.filename:
            return

        self.inv = read_inventory(self.filename)
        self.plot_inv()

    def plot_inv(self):
        for i, station in enumerate(self.inv[0]):
            js_call = "addStation('{station_id}', {latitude}, {longitude});" \
                .format(station_id=station.code, latitude=station.latitude,
                        longitude=station.longitude)
            self.view.page().mainFrame().evaluateJavaScript(js_call)

if __name__ == '__main__':
    proxy_queary = query_yes_no("Input Proxy Settings?")
    print('')

    if proxy_queary == 'yes':
        proxy = raw_input("Proxy:")
        port = raw_input("Proxy Port:")
        try:
            networkProxy = QtNetwork.QNetworkProxy(QtNetwork.QNetworkProxy.HttpProxy, proxy, int(port))
            QtNetwork.QNetworkProxy.setApplicationProxy(networkProxy)
        except ValueError:
            print('No proxy settings supplied..')
            sys.exit()

    app = QtGui.QApplication([])
    w = MainWindow()
    w.raise_()
    app.exec_()