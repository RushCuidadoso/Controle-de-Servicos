#!/usr/bin/python
# -*- coding: latin-1 -*-

from PyQt5 import QtGui, QtCore, QtWidgets
import sys
import psycopg2
import frmpessoas
from codeconexion import conexion

class pessoasApp(QtWidgets.QMainWindow, frmpessoas.Ui_frmpessoas):
    conexion = conexion()
    caller = None
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.btnclientes.clicked.connect(self.llamarcliente)
        self.btnfuncio.clicked.connect(self.llamarfuncio)
        self.btnfornecedor.clicked.connect(self.llamarprov)

    def iniciar(self, caller):
        self.caller = caller
        # self.caller.setEnabled(False)

    def closeEvent(self, *args, **kwargs):
        self.caller.setEnabled(True)

    def llamarcliente(self):
        self.setEnabled(False)
        from codecliente import clienteApp
        self.cliente = clienteApp(parent=self)
        self.cliente.show()
        self.cliente.iniciar(self, 1)

    def llamarfuncio(self):
        self.setEnabled(False)
        from codefuncionario import funcionarioApp
        self.funcio = funcionarioApp(parent=self)
        self.funcio.show()
        self.funcio.iniciar(self, 1)

    def llamarprov(self):
        self.setEnabled(False)
        from codefornecedor import fornecedorApp
        self.prov = fornecedorApp(parent=self)
        self.prov.show()
        self.prov.iniciar(self, 1)

def main():
    app = QtWidgets.QApplication(sys.argv)
    form = pessoasApp()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()