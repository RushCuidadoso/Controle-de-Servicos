#!/usr/bin/python
# -*- coding: latin-1 -*-

from PyQt5 import QtGui, QtCore, QtWidgets
import sys
import psycopg2
import frmfuncio
from codeconexion import conexion

class funcionarioApp(QtWidgets.QMainWindow, frmfuncio.Ui_frmfuncio):
    conexion = conexion()
    caller = None
    buscar="'%%'"
    cod=0
    sumalinea=0
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.consultar()
        self.cancelar()
        self.btnnovo.clicked.connect(self.nuevo)
        self.btncancelar.clicked.connect(self.cancelar)
        self.btnsalvar.clicked.connect(self.guardar)
        self.btneditar.clicked.connect(self.editar)
        self.btneliminar.clicked.connect(self.eliminar)
        self.tabla.cellClicked.connect(self.cargar)
        self.txtbuscar.textChanged.connect(self.fbuscar)
        self.tabla.cellDoubleClicked.connect(self.devolver)
        self.txtnom.returnPressed.connect(self.totel)
        self.txttel.returnPressed.connect(self.torg)
        self.txtrg.returnPressed.connect(self.tocpf)
        self.txtcpf.returnPressed.connect(self.tobtnsalvar)
        self.btnsalvar.setAutoDefault(True)

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_F1:
                self.nuevo()

    def totel(self):
        self.txttel.setFocus()

    def torg(self):
        self.txtrg.setFocus()

    def tocpf(self):
        self.txtcpf.setFocus()

    def tobtnsalvar(self):
        self.btnsalvar.setFocus()

    def iniciar(self,caller, menu):
        self.menu = menu
        self.caller = caller

    def closeEvent(self, *args, **kwargs):
        self.caller.setEnabled(True)
        if self.menu != 1:
            self.caller.txtcodfuncio.setFocus()

    def devolver(self):
        if self.menu == 0:
            self.caller.setEnabled(True)
            self.caller.txtcodfuncio.setText(str(self.txtcod.text()))
            self.caller.consultafuncio()
            self.close()

    def consultar(self):
        con = None
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select count(*) from funcionario where nomfuncio like' + self.buscar)
        rows = cur.fetchone()

        if (int(rows[0]) > 0):
            self.lblsinreg.setVisible(False)
            self.config(rows)
            cur.execute(
                'select codfuncio, nomfuncio, telefone, rg, cpf from funcionario where nomfuncio like' + self.buscar + ' order by codfuncio asc')
            self.cliente = cur.fetchall()

            for i in range(int(rows[0])):
                item = self.cliente[i]
                cod = QtWidgets.QTableWidgetItem(str(item[0]))
                nom = QtWidgets.QTableWidgetItem(str(item[1]))
                telefone = QtWidgets.QTableWidgetItem(str(item[2]))
                rg = QtWidgets.QTableWidgetItem(str(item[3]))
                cpf = QtWidgets.QTableWidgetItem(str(item[4]))
                self.tabla.setItem(i, 0, cod)
                self.tabla.setItem(i, 1, nom)
                self.tabla.setItem(i, 2, telefone)
                self.tabla.setItem(i, 3, rg)
                self.tabla.setItem(i, 4, cpf)
        else:
            self.lblsinreg.setVisible(True)
            self.tabla.setRowCount(0)
            self.tabla.setColumnCount(0)

    def fbuscar(self):
        buscado=str(self.txtbuscar.text())
        if len(buscado)>0:
            self.buscar="'%"+buscado+"%'"
            #print self.buscar
        else:
            self.buscar="'%%'"
        self.consultar()

    def config(self,rows):
        lista = 'Codigo', 'Funcionario', 'Telefone', 'RG', 'CPF'
        self.tabla.setColumnCount(5)
        self.tabla.setRowCount(int(rows[0]))
        self.tabla.setHorizontalHeaderLabels(lista)
        # self.tabla.setColumnWidth(0,50)
        # self.tabla.setColumnWidth(1,319)
        header = self.tabla.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)

    def cargar(self):
        self.cancelar()
        index = int(self.lblindice.text())
        item = self.cliente[index]
        self.txtcod.setText(str(item[0]))
        self.txtnom.setText(str(item[1]))
        self.txttel.setText(str(item[2]))
        self.txtrg.setText(str(item[3]))
        self.txtcpf.setText(str(item[4]))
        self.btnsalvar.setVisible(False)
        self.btneditar.setVisible(True)
        self.btneditar.setEnabled(True)
        self.btneliminar.setEnabled(True)

    def nuevo(self):
        # al clicar en el boton se prepara para guardar una informacion
        self.cancelar()
        self.bnd = 0
        self.txtnom.setEnabled(True)
        self.txttel.setEnabled(True)
        self.txtrg.setEnabled(True)
        self.txtcpf.setEnabled(True)
        self.txtnom.setFocus()
        self.btnnovo.setEnabled(False)
        self.btneditar.setVisible(False)
        self.btneditar.setEnabled(False)
        self.btnsalvar.setVisible(True)
        self.btnsalvar.setEnabled(True)
        self.btneliminar.setEnabled(False)
        self.btncancelar.setEnabled(True)

    def editar(self):
        self.bnd=1
        self.txtnom.setEnabled(True)
        self.txttel.setEnabled(True)
        self.txtrg.setEnabled(True)
        self.txtcpf.setEnabled(True)
        self.txtnom.setFocus()
        self.btnnovo.setEnabled(False)
        self.btneditar.setVisible(False)
        self.btneditar.setEnabled(False)
        self.btnsalvar.setVisible(True)
        self.btnsalvar.setEnabled(True)
        self.btneliminar.setEnabled(False)
        self.btncancelar.setEnabled(True)

    def cancelar(self):
        self.txtcod.setEnabled(False)
        self.txtnom.setEnabled(False)
        self.txttel.setEnabled(False)
        self.txtrg.setEnabled(False)
        self.txtcpf.setEnabled(False)
        self.txtcod.clear()
        self.txtnom.clear()
        self.txttel.clear()
        self.txtrg.clear()
        self.txtcpf.clear()
        self.btnnovo.setEnabled(True)
        self.btneditar.setVisible(False)
        self.btneditar.setEnabled(False)
        self.btnsalvar.setVisible(True)
        self.btnsalvar.setEnabled(False)
        self.btneliminar.setEnabled(True)
        self.btncancelar.setEnabled(False)

    def eliminar(self):
        cod = int(self.txtcod.text())
        #con = None
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select count(*) from servicio where codfuncio=%s',[cod])
        rows = cur.fetchone()
        if int(rows[0])==0:
            mensaje = QtGui.QMessageBox.question(self, "Eliminando Registro", "Deseja Eliminar este Registro?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if (mensaje == QtGui.QMessageBox.Yes):
                con = self.conexion.conectar()
                cur = con.cursor()
                cur.execute('delete from funcionario where codfuncio = %s', [cod])
                con.commit()
                self.cancelar()
                self.consultar()
                mensaje = QtGui.QMessageBox.information(self, "Eliminando Registro", "Registro Eliminado", QtGui.QMessageBox.Ok)
        else:
            mensaje = QtGui.QMessageBox.question(self, "Error ao eliminar registro", "Esse registro tem um serviço registrado",QtGui.QMessageBox.Ok)

    def guardar(self):
        if len(self.txtcod.text()) > 0:
            cod = str(self.txtcod.text())
        nom = str(self.txtnom.text())
        tel = str(self.txttel.text())
        if len(tel)==0:
            tel='Vazio'
        rg = str(self.txtrg.text())
        if len(rg)==0:
            rg='Vazio'
        cpf = str(self.txtcpf.text())
        if len(cpf)==0:
            cpf='Vazio'
        if (len(nom) > 1):
            con = self.conexion.conectar()
            cur = con.cursor()
            if self.bnd == 0:
                cur.execute(
                    'insert into funcionario (nomfuncio, telefone, rg, cpf) values(%s,%s,%s,%s)', [nom, tel, rg, cpf])
                con.commit()
                self.cancelar()
                self.consultar()
                row=self.tabla.rowCount()
                self.tabla.selectRow(row-1)
            else:
                cur.execute('update funcionario set nomfuncio=%s, telefone=%s, rg=%s, cpf=%s where codfuncio=%s', [nom, tel, rg, cpf, cod])
                con.commit()
                self.cancelar()
                self.consultar()
        else:
            mensaje = QtGui.QMessageBox.information(self, "Caracteres insuficientes","Um campo nao cumpre os requisitos", QtGui.QMessageBox.Ok)

def main():
    app = QtWidgets.QApplication(sys.argv)
    form = funcionarioApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()