#!/usr/bin/python
# -*- coding: latin-1 -*-

from PyQt5 import QtGui, QtCore, QtWidgets
import sys
import psycopg2
import frmfornecedor
from codeconexion import conexion

class fornecedorApp(QtWidgets.QMainWindow, frmfornecedor.Ui_frmfornecedor):
    conexion = conexion()
    caller = None
    buscar="'%%'"
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)    
        self.bnd=0
        self.consultar()
        self.cancelar()
        self.txtbuscar.textChanged.connect(self.fbuscar)          
        self.btnnovo.clicked.connect(self.nuevo)
        self.btncancelar.clicked.connect(self.cancelar)
        self.tabla.cellDoubleClicked.connect(self.devolver)
        self.tabla.cellClicked.connect(self.cargar)
        self.btneditar.clicked.connect(self.editar)
        self.btnsalvar.clicked.connect(self.guardar)
        self.lblindice.setVisible(False)
        self.btneliminar.clicked.connect(self.eliminar)
        self.btnrepre.clicked.connect(self.llamarrepre)
        self.txtnom.returnPressed.connect(self.tobtnsalvar)
        self.btnsalvar.setAutoDefault(True)

    def tobtnsalvar(self):
        self.btnsalvar.setFocus()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_F1:
                self.nuevo()

    def closeEvent(self, *args, **kwargs):
        self.caller.setEnabled(True)
        if self.menu != 1:
            self.caller.txtcodproveedor.setFocus()

    def iniciar(self,caller, menu):
        self.caller = caller
        self.menu = menu

    def devolver(self):
        if self.menu == 0:
            self.caller.setEnabled(True)

            self.caller.consultarfornecedor(str(self.txtcod.text()))
            self.close()

    def llamarrepre(self):
        # self.cerrar=1
        from coderepresentante import representanteApp
        self.setEnabled(False)
        self.representante = representanteApp(parent=self)
        self.representante.show()
        self.representante.iniciar(self,self.txtcod.text(),self.txtnom.text())
        # self indica el caller en el otro codigo, indica que fue este codigo que llamo el otro codigo
        
    def nuevo(self):
        #al clicar en el boton se prepara para guardar una informacion
        self.cancelar()
        self.bnd=0
        self.txtnom.setEnabled(True)
        self.txtnom.setFocus()
        self.btnnovo.setEnabled(False)
        self.btneditar.setVisible(False)
        self.btneditar.setEnabled(False)
        self.btnsalvar.setVisible(True)
        self.btnsalvar.setEnabled(True)
        self.btneliminar.setEnabled(False)
        self.btncancelar.setEnabled(True)
        
    def cancelar(self):
        self.txtnom.setEnabled(False)
        self.txtnom.clear()
        self.txtcod.clear()
        self.btnnovo.setEnabled(True)
        self.btneditar.setVisible(False)
        self.btnsalvar.setEnabled(False)
        self.btnsalvar.setVisible(True)
        self.btneliminar.setEnabled(False)
        self.btncancelar.setEnabled(False)
        self.btnrepre.setEnabled(False)

        
    def fbuscar(self):
        buscado=str(self.txtbuscar.text())
        if len(buscado)>0:
            self.buscar="'%"+buscado+"%'"
            #print self.buscar
        else:
            self.buscar="'%%'"
        self.consultar()      
        
    def editar(self):
        self.bnd=1
        self.txtnom.setEnabled(True)
        self.txtnom.setFocus()
        self.btnnovo.setEnabled(False)
        self.btneditar.setVisible(False)
        self.btnsalvar.setEnabled(True)
        self.btnsalvar.setVisible(True)
        self.btneliminar.setEnabled(False)
        self.btncancelar.setEnabled(True)        
        
    def cargar(self):
        self.cancelar()
        index = int(self.lblindice.text())
        item = self.fornecedor[index]
        self.txtcod.setText(str(item[0]))
        self.txtnom.setText(str(item[1]))
        self.btnsalvar.setVisible(False)
        self.btneditar.setVisible(True)
        self.btneditar.setEnabled(True)
        self.btneliminar.setEnabled(True)
        self.btnrepre.setEnabled(True)
        
    def guardar(self):
        if len(self.txtcod.text()) > 0:
            cod = str(self.txtcod.text())
        nom = (self.txtnom.text())
        if (len(nom) > 1):
            con = self.conexion.conectar()
            cur = con.cursor()
            if self.bnd == 0:
                cur.execute(
                    'insert into fornecedor (nomfornecedor) values(%s)', [nom])
                con.commit()                
                self.cancelar()
                self.consultar()                
                row=self.tabla.rowCount()
                self.tabla.selectRow(row-1)                
            else:
                cur.execute('update fornecedor set nomfornecedor=%s where codfornecedor=%s', [nom, cod])
                con.commit()
                self.cancelar()
                self.consultar()
        else:
            mensaje = QtGui.QMessageBox.information(self, "Caracteres insuficientes","Um campo nao cumpre os requisitos", QtGui.QMessageBox.Ok)
            self.txtnom.setFocus()

    def consultar(self):
        con = None
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select count(*) from fornecedor where nomfornecedor like' + self.buscar)
        rows = cur.fetchone()

        if (int(rows[0]) > 0):
            self.lblsinreg.setVisible(False)
            self.config(rows)
            cur.execute(
                'select codfornecedor, nomfornecedor from fornecedor where nomfornecedor like' + self.buscar + ' order by codfornecedor asc')
            self.fornecedor = cur.fetchall()

            for i in range(int(rows[0])):
                item = self.fornecedor[i]
                cod = QtWidgets.QTableWidgetItem(str(item[0]))
                fornecedor = QtWidgets.QTableWidgetItem(str(item[1]))
                self.tabla.setItem(i, 0, cod)
                self.tabla.setItem(i, 1, fornecedor)
        else:
            self.lblsinreg.setVisible(True)
            self.tabla.setRowCount(0)
            self.tabla.setColumnCount(0)

    def config(self,rows):
        lista = 'Codigo', 'Fornecedor'
        self.tabla.setColumnCount(2)
        self.tabla.setRowCount(int(rows[0]))
        self.tabla.setHorizontalHeaderLabels(lista)
        self.tabla.setColumnWidth(0,50)
        self.tabla.setColumnWidth(1,319)
        header = self.tabla.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
            
    def eliminar(self):
        cod = int(self.txtcod.text())
        #con = None
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select count(*) from representante where codfornecedor=%s',[cod])
        rows = cur.fetchone()
        if int(rows[0])==0:
            mensaje = QtGui.QMessageBox.question(self, "Eliminando Registro", "Deseja Eliminar este Registro?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if (mensaje == QtGui.QMessageBox.Yes):
                con = self.conexion.conectar()
                cur = con.cursor()
                cur.execute('delete from fornecedor where codfornecedor = %s', [cod])
                con.commit()
                self.cancelar()
                self.consultar()
                mensaje = QtGui.QMessageBox.information(self, "Eliminando Registro", "Registro Eliminado", QtGui.QMessageBox.Ok)
        else:
            mensaje = QtGui.QMessageBox.question(self, "Error ao eliminar registro", "Esse registro tem uma representante registrado",QtGui.QMessageBox.Ok)
        
def main():
    app = QtWidgets.QApplication(sys.argv)
    form = fornecedorApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()    