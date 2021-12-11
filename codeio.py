#!/usr/bin/python
# -*- coding: latin-1 -*-

from PyQt5 import QtGui, QtCore, QtWidgets
import sys
import psycopg2
import frmio
from codeconexion import conexion

class ioApp(QtWidgets.QMainWindow, frmio.Ui_frmio):
    conexion = conexion()
    caller = None
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.btnentrada.clicked.connect(self.llamarentrada)
        self.btnsaida.clicked.connect(self.llamarsalida)
        self.btnlista.clicked.connect(self.llamarlista)

    def iniciar(self, caller):
        self.caller = caller
        # self.caller.setEnabled(False)

    def closeEvent(self, *args, **kwargs):
        self.caller.setEnabled(True)

    def llamarentrada(self):
        self.setEnabled(False)
        from codeentrada import entradaApp
        self.entrada = entradaApp(parent=self)
        self.entrada.show()
        self.entrada.iniciar(self)

    def llamarsalida(self):
        self.setEnabled(False)
        from codeservicio import servicioApp
        self.servicio = servicioApp(parent=self)
        self.servicio.show()
        self.servicio.iniciar(self)

    def llamarlista(self):
        self.setEnabled(False)
        from codelista import listaApp
        self.lista = listaApp(parent=self)
        self.lista.show()
        self.lista.iniciar(self,0)

def main():
    app = QtWidgets.QApplication(sys.argv)
    form = ioApp()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()