#!/usr/bin/python
# -*- coding: latin-1 -*-

from PyQt5 import QtGui, QtCore, QtWidgets
import sys
import psycopg2
import frmequipamento
from codeconexion import conexion


class equipApp(QtWidgets.QMainWindow, frmequipamento.Ui_frmequip):
    conexion = conexion()
    caller = None
    buscar = "'%%'"
    entertabla = 0
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.bnd = 0
        self.consultar()
        self.cancelar()
        self.txtbuscar.textChanged.connect(self.fbuscar)
        self.btnnovo.clicked.connect(self.nuevo)
        self.btncancelar.clicked.connect(self.cancelar)
        self.tabla.cellDoubleClicked.connect(self.devolver)
        self.btnmarca.clicked.connect(self.llamarmarca)
        self.tabla.cellClicked.connect(self.cargar)
        self.btneditar.clicked.connect(self.editar)
        self.btnsalvar.clicked.connect(self.guardar)
        self.lblindice.setVisible(False)
        self.btneliminar.clicked.connect(self.eliminar)
        self.txtbuscar.returnPressed.connect(self.totabla)
        self.tabla.itemSelectionChanged.connect(self.cargar)
        self.txtnom.returnPressed.connect(self.tomarca)
        self.btnmarca.setAutoDefault(True)
        self.btnsalvar.setAutoDefault(True)

    def totabla(self):
        self.tabla.setFocus()
        self.tabla.selectRow(0)

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_F1:
            self.nuevo()
        if self.tabla.hasFocus():
            if e.key() == QtCore.Qt.Key_Return or e.key() == QtCore.Qt.Key_Enter:
                if self.entertabla == 1:
                    self.entertabla = 0
                    self.devolver()
                else:
                    self.entertabla = 1

    def tomarca(self):
        self.btnmarca.setFocus()

    def closeEvent(self, *args, **kwargs):
        self.caller.setEnabled(True)
        if not self.menu == 0:
            self.caller.txtcodequip.setFocus()

    def iniciar(self, caller, menu):
        self.caller = caller
        self.menu = menu

    def devolver(self):
        # self.caller.setEnabled(True)
        if self.menu !=0:
            self.caller.txtcodequip.setText((str(self.txtcod.text())))
            self.caller.consultaequip()
            self.close()

    def llamarmarca(self):
        # self.cerrar=1
        from codemarca import marcaApp
        self.marca = marcaApp(parent=self)
        estado = 1
        self.marca.show()
        # inserir condigo para evitar que el resto del sistema pueda usarse desabilitado
        self.marca.iniciar(self, 1)
        # self indica el caller en el otro codigo, indica que fue este codigo que llamo el otro codigo
        # self.marca.iniciar(self.caller)

    def consultarmarca(self, codmarca):
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select codmarca, nommarca from marca where codmarca=' + codmarca)
        item = cur.fetchall()
        var = item[0]
        self.codmarca.setText(str(var[0]))
        self.txtmarca.setText(str(var[1]))
        self.btnsalvar.setFocus()


    def nuevo(self):
        # al clicar en el boton se prepara para guardar una informacion
        self.cancelar()
        self.bnd = 0
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
        self.txtmarca.clear()
        self.btnnovo.setEnabled(True)
        self.btneditar.setVisible(False)
        self.btnsalvar.setEnabled(False)
        self.btnsalvar.setVisible(True)
        self.btneliminar.setEnabled(False)
        self.btncancelar.setEnabled(False)
        self.entertabla=0

    def fbuscar(self):
        buscado = str(self.txtbuscar.text())
        if len(buscado) > 0:
            self.buscar = "'%" + buscado + "%'"
            # print self.buscar
        else:
            self.buscar = "'%%'"
        self.consultar()

    def editar(self):
        self.bnd = 1
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
        # index = int(self.lblindice.text())
        index = self.tabla.currentRow()
        item = self.equip[index]
        self.txtcod.setText(str(item[0]))
        self.txtnom.setText(str(item[1]))
        self.codmarca.setText(str(item[5]))
        self.txtmarca.setText(str(item[2]))
        modelo = item[3]
        ciclagem = item[4]
        if modelo==4:
            self.radnd1.setChecked(True)
        elif modelo==5:
            self.radmono.setChecked(True)
        elif modelo==6:
            self.radtri.setChecked(True)
        if ciclagem==1:
            self.radnd2.setChecked(True)
        elif ciclagem==2:
            self.rad50.setChecked(True)
        elif ciclagem==3:
            self.rad60.setChecked(True)
        self.btnsalvar.setVisible(False)
        self.btneditar.setVisible(True)
        self.btneditar.setEnabled(True)
        self.btneliminar.setEnabled(True)

    def modelociclagem(self,var):
        if var == 1:
            var = "Não Disponível"
        elif var == 2:
            var = '50Hz'
        elif var == 3:
            var = '60Hz'

        if var == 4:
            var = "Não Disponível"
        elif var == 5:
            var = 'Monofásico'
        elif var == 6:
            var = 'Trifásico'
        return var

    def guardar(self):
        if len(self.txtcod.text()) > 0:
            cod = str(self.txtcod.text())
        nom = str(self.txtnom.text())
        codmarca = str(self.codmarca.text())
        if len(codmarca) == 0:
            codmarca = '9999999'
        if self.radnd2.isChecked():
            ciclagem = 1
        elif self.rad50.isChecked():
            ciclagem = 2
        elif self.rad60.isChecked():
            ciclagem = 3

        if self.radnd1.isChecked():
            modelo = 4
        elif self.radmono.isChecked():
            modelo = 5
        elif self.radtri.isChecked():
            modelo = 6

        if (len(nom) > 1):
            con = self.conexion.conectar()
            cur = con.cursor()
            if self.bnd == 0:
                cur.execute(
                    'insert into equipamento (nomequip, codmarca, modelo, ciclagem) values(%s,%s,%s,%s)', [nom, codmarca, modelo, ciclagem])
                con.commit()
                self.cancelar()
                self.consultar()
                row = self.tabla.rowCount()
                self.tabla.selectRow(row - 1)
            else:
                cur.execute('update equipamento set nomequip=%s, codmarca=%s, modelo=%s, ciclagem=%s where codequip=%s', [nom, codmarca, modelo, ciclagem, cod])
                con.commit()
                self.cancelar()
                self.consultar()
        else:
            mensaje = QtGui.QMessageBox.information(self, "Caracteres insuficientes",
                                                    "Um campo nao cumpre os requisitos", QtGui.QMessageBox.Ok)
            self.txtnom.setFocus()

    def consultar(self):
        con = None
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select count(*) from equipamento where nomequip like' + self.buscar)
        rows = cur.fetchone()

        if (int(rows[0]) > 0):
            self.lblsinreg.setVisible(False)
            self.config(rows)
            cur.execute(
                'select a.codequip, a.nomequip, b.nommarca, a.modelo, a.ciclagem, a.codmarca from equipamento a, marca b where a.codmarca=b.codmarca and a.nomequip like' + self.buscar + ' order by a.codequip asc')
            self.equip = cur.fetchall()

            for i in range(int(rows[0])):
                item = self.equip[i]
                cod = QtWidgets.QTableWidgetItem(str(item[0]))
                nom = QtWidgets.QTableWidgetItem(str(item[1]))
                marca = QtWidgets.QTableWidgetItem(str(item[2]))
                self.tabla.setItem(i, 0, cod)
                self.tabla.setItem(i, 1, nom)
                self.tabla.setItem(i, 2, marca)
                modelo = self.modelociclagem(item[3])
                self.tabla.setItem(i, 3, QtWidgets.QTableWidgetItem(str(modelo)))
                ciclagem = self.modelociclagem(item[4])
                self.tabla.setItem(i, 4, QtWidgets.QTableWidgetItem(str(ciclagem)))
        else:
            self.lblsinreg.setVisible(True)
            self.tabla.setRowCount(0)
            self.tabla.setColumnCount(0)

    def config(self, rows):
        lista = 'Codigo', 'Equipamento', 'Marca', 'Modelo', 'Ciclagem'
        self.tabla.setColumnCount(5)
        self.tabla.setRowCount(int(rows[0]))
        self.tabla.setHorizontalHeaderLabels(lista)
        # self.tabla.setColumnWidth(0, 50)
        # self.tabla.setColumnWidth(1, 319)
        header = self.tabla.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)

    def eliminar(self):
        cod = int(self.txtcod.text())
        # con = None
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select count(*) from servi where codequip=%s', [cod])
        rows = cur.fetchone()
        if int(rows[0]) == 0:
            mensaje = QtGui.QMessageBox.question(self, "Eliminando Registro", "Deseja Eliminar este Registro?",
                                                 QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if (mensaje == QtGui.QMessageBox.Yes):
                con = self.conexion.conectar()
                cur = con.cursor()
                cur.execute('delete from equipamento where codequip = %s', [cod])
                con.commit()
                self.cancelar()
                self.consultar()
                mensaje = QtGui.QMessageBox.information(self, "Eliminando Registro", "Registro Eliminado",
                                                        QtGui.QMessageBox.Ok)
        else:
            mensaje = QtGui.QMessageBox.question(self, "Error ao eliminar registro",
                                                 "Esse registro tem uma representante registrado", QtGui.QMessageBox.Ok)


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = equipApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()