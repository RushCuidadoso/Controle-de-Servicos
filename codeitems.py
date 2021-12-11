#!/usr/bin/python
# -*- coding: latin-1 -*-

from PyQt5 import QtGui, QtCore, QtWidgets
import sys
import psycopg2
import frmitems
from codeconexion import conexion

class itemsApp(QtWidgets.QMainWindow, frmitems.Ui_frmitems):
    conexion = conexion()
    caller = None
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.btnmarca.clicked.connect(self.llamarmarcas)
        self.btnmedida.clicked.connect(self.llamarmedidas)
        self.btnproduto.clicked.connect(self.llamarproduto)
        self.btnequip.clicked.connect(self.llamarequip)

    def iniciar(self, caller):
        self.caller = caller
        # self.caller.setEnabled(False)

    def closeEvent(self, *args, **kwargs):
        self.caller.setEnabled(True)

    def llamarmarcas(self):
        self.setEnabled(False)
        from codemarca import marcaApp
        self.marca = marcaApp(parent=self)
        self.marca.show()
        self.marca.iniciar(self, 0)

    def llamarmedidas(self):
        self.setEnabled(False)
        from codemedida import medidaApp
        self.medida = medidaApp(parent=self)
        self.medida.show()
        self.medida.iniciar(self, 0)

    def llamarproduto(self):
        self.setEnabled(False)
        from codeproducto import productoApp
        self.producto = productoApp(parent=self)
        self.producto.show()
        self.producto.iniciar(self, 0)

    def llamarequip(self):
        self.setEnabled(False)
        from codeequip import equipApp
        self.equip = equipApp(parent=self)
        self.equip.show()
        self.equip.iniciar(self, 0)

def main():
    app = QtWidgets.QApplication(sys.argv)
    form = itemsApp()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()