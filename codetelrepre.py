from PyQt5 import QtGui, QtCore, QtWidgets
import sys
import psycopg2
import frmtelrepre
from codeconexion import conexion

class telrepreApp(QtWidgets.QMainWindow, frmtelrepre.Ui_frmtelrepre):
    conexion = conexion()
    caller = None
    buscar="'%%'"
    cod=0
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        # self.consultar()
        self.cancelar()
        self.txtbuscar.textChanged.connect(self.fbuscar)
        self.btnnovo.clicked.connect(self.nuevo)
        self.btncancelar.clicked.connect(self.cancelar)
        # self.tabla.cellDoubleClicked.connect(self.devolver)
        self.tabla.cellClicked.connect(self.cargar)
        self.btneditar.clicked.connect(self.editar)
        self.btnsalvar.clicked.connect(self.guardar)
        self.lblindice.setVisible(False)
        self.btneliminar.clicked.connect(self.eliminar)
        self.txttelefone.returnPressed.connect(self.tobtnsalvar)
        self.btnsalvar.setAutoDefault(True)

    def tobtnsalvar(self):
        self.btnsalvar.setFocus()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_F1:
                self.nuevo()


    def iniciar(self, caller, cod, repre):
        self.caller = caller
        self.cod = cod
        self.txtrepre.setText(repre)
        self.consultar()
        self.nuevo()
        # self.cerrar=0

    def closeEvent(self, evnt):
        # if not self.cerrar==1:
        self.caller.setEnabled(True)

    def nuevo(self):
        # al clicar en el boton se prepara para guardar una informacion
        self.cancelar()
        self.bnd = 0
        self.txttelefone.setEnabled(True)
        self.txttelefone.setFocus()
        self.btnnovo.setEnabled(False)
        self.btneditar.setVisible(False)
        self.btneditar.setEnabled(False)
        self.btnsalvar.setVisible(True)
        self.btnsalvar.setEnabled(True)
        self.btneliminar.setEnabled(False)
        self.btncancelar.setEnabled(True)

    def cancelar(self):
        self.txtcod.clear()
        self.txttelefone.clear()
        self.txttelefone.setEnabled(False)
        self.btnnovo.setEnabled(True)
        self.btneditar.setVisible(False)
        self.btnsalvar.setEnabled(False)
        self.btnsalvar.setVisible(True)
        self.btneliminar.setEnabled(False)
        self.btncancelar.setEnabled(False)

    def fbuscar(self):
        buscado = str(self.txtbuscar.text())
        if len(buscado) > 0:
            self.buscar = "'%" + buscado + "%'"
        else:
            self.buscar = "'%%'"
        self.consultar()

    def editar(self):
        self.bnd = 1
        self.txttelefone.setEnabled(True)
        self.txttelefone.setFocus()
        self.btnnovo.setEnabled(False)
        self.btneditar.setVisible(False)
        self.btnsalvar.setEnabled(True)
        self.btnsalvar.setVisible(True)
        self.btneliminar.setEnabled(False)
        self.btncancelar.setEnabled(True)

    def guardar(self):
        if len(self.txtcod.text()) > 0:
            codigo = str(self.txtcod.text())
        num = str(self.txttelefone.text())
        cod = str(self.cod)
        if (len(num) > 1):
            con = self.conexion.conectar()
            cur = con.cursor()
            if self.bnd == 0:
                cur.execute('insert into telrepre (numtel, codrepre) values(%s,%s)', [num, cod])
                con.commit()
                self.cancelar()
                self.consultar()
                row = self.tabla.rowCount()
                self.tabla.selectRow(row - 1)
            else:
                cur.execute('update telrepre set numtel=%s, codrepre=%s where codtel=%s',
                            [num, str(self.cod), codigo])
                con.commit()
                self.cancelar()
                self.consultar()
        else:
            mensaje = QtGui.QMessageBox.information(self, "Caracteres insuficientes",
                                                    "Um campo nao cumpre os requisitos", QtGui.QMessageBox.Ok)
            self.txttelefone.setFocus()

    def consultar(self):
        con = None
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select count(*) from telrepre where codrepre=' + str(self.cod) + ' and numtel like' + self.buscar)
        rows = cur.fetchone()

        if (int(rows[0]) > 0):
            self.lblsinreg.setVisible(False)
            self.config(rows)
            cur.execute(
                'select a.codtel, a.numtel, b.nomrepre, c.nomfornecedor from telrepre a, representante b, fornecedor '
                'c where a.codrepre=b.codrepre and b.codfornecedor=c.codfornecedor and a.codrepre=' + str(self.cod) + ' and a.numtel like' + self.buscar + 'order by a.codtel asc')
            self.telrepre = cur.fetchall()

            for i in range(int(rows[0])):
                item = self.telrepre[i]
                cod = QtGui.QTableWidgetItem(str(item[0]))
                tel = QtGui.QTableWidgetItem(str(item[1]))
                repre = QtGui.QTableWidgetItem(str(item[2]))
                fornecedor = QtGui.QTableWidgetItem(str(item[3]))
                self.tabla.setItem(i, 0, cod)
                self.tabla.setItem(i, 1, tel)
                self.tabla.setItem(i, 2, repre)
                self.tabla.setItem(i, 3, fornecedor)
        else:
            self.lblsinreg.setVisible(True)
            self.tabla.setRowCount(0)
            self.tabla.setColumnCount(0)

    def cargar(self):
        self.cancelar()
        index = int(self.lblindice.text())
        item = self.telrepre[index]
        self.txtcod.setText(str(item[0]))
        self.txttelefone.setText(str(item[1]))
        self.btnsalvar.setVisible(False)
        self.btneditar.setVisible(True)
        self.btneditar.setEnabled(True)
        self.btneliminar.setEnabled(True)

    def config(self, rows):
        lista = 'Codigo', 'Telefone', 'Representante', 'Fornecedor'
        self.tabla.setColumnCount(4)
        self.tabla.setRowCount(int(rows[0]))
        self.tabla.setHorizontalHeaderLabels(lista)
        # self.tabla.setColumnWidth(0, 50)
        # self.tabla.setColumnWidth(1, 319)
        header = self.tabla.horizontalHeader()
        header.setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(1, QtGui.QHeaderView.Stretch)
        header.setResizeMode(2, QtGui.QHeaderView.Stretch)
        header.setResizeMode(3, QtGui.QHeaderView.Stretch)

    def eliminar(self):
        cod = int(self.txtcod.text())
        # con = None
        # con = self.conexion.conectar()
        # cur = con.cursor()
        # cur.execute('select count(*) from telrepre where codrepresentante=%s', [cod])
        # rows = cur.fetchone()
        # if int(rows[0]) == 0:
        mensaje = QtGui.QMessageBox.question(self, "Eliminando Registro", "Deseja Eliminar este Registro?",
                                             QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if (mensaje == QtGui.QMessageBox.Yes):
            con = self.conexion.conectar()
            cur = con.cursor()
            cur.execute('delete from telrepre where codtel = %s', [cod])
            con.commit()
            self.cancelar()
            self.consultar()
            mensaje = QtGui.QMessageBox.information(self, "Eliminando Registro", "Registro Eliminado",
                                                    QtGui.QMessageBox.Ok)




def main():
    app = QtWidgets.QApplication(sys.argv)
    form = telrepreApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()