from PyQt5 import QtGui, QtCore, QtWidgets
import sys
import psycopg2
import frmrepresentante
from codeconexion import conexion

class representanteApp(QtWidgets.QMainWindow, frmrepresentante.Ui_frmrepresentante):
    conexion = conexion()
    caller = None
    buscar="'%%'"
    cod=0
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.bnd=0
        # self.consultar()
        self.cancelar()
        self.txtbuscar.textChanged.connect(self.fbuscar)
        self.btnnovo.clicked.connect(self.nuevo)
        self.btncancelar.clicked.connect(self.cancelar)
        #self.tabla.cellDoubleClicked.connect(self.devolver)
        self.tabla.cellClicked.connect(self.cargar)
        self.btneditar.clicked.connect(self.editar)
        self.btnsalvar.clicked.connect(self.guardar)
        self.lblindice.setVisible(False)
        self.btneliminar.clicked.connect(self.eliminar)
        self.btntelrepre.clicked.connect(self.llamartelrepre)

        self.txtrepre.returnPressed.connect(self.toemail)
        self.txtemail.returnPressed.connect(self.tobtnsalvar)
        self.btnsalvar.setAutoDefault(True)

    def toemail(self):
        self.txtemail.setFocus()

    def tobtnsalvar(self):
        self.btnsalvar.setFocus()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_F1:
                self.nuevo()

    def llamartelrepre(self):
        # self.cerrar=1
        from codetelrepre import telrepreApp
        self.setEnabled(False)
        self.telrepre = telrepreApp(parent=self)
        self.telrepre.show()
        # inserir codigo para evitar que el resto del sistema pueda usarse desabilitado
        self.telrepre.iniciar(self,self.txtcod.text(),self.txtrepre.text())
        # self indica el caller en el otro codigo, indica que fue este codigo que llamo el otro codigo

    def iniciar(self,caller,cod,fornecedor):
        self.caller=caller
        self.cod=cod
        self.txtfornecedor.setText(fornecedor)
        self.consultar()
        self.nuevo()
        #self.cerrar=0

    def closeEvent(self, evnt):
        # if not self.cerrar==1:
            self.caller.setEnabled(True)

    def nuevo(self):
        # al clicar en el boton se prepara para guardar una informacion
        self.cancelar()
        self.bnd = 0
        self.txtrepre.setEnabled(True)
        self.txtrepre.setFocus()
        self.txtemail.setEnabled(True)
        self.btnnovo.setEnabled(False)
        self.btneditar.setVisible(False)
        self.btneditar.setEnabled(False)
        self.btnsalvar.setVisible(True)
        self.btnsalvar.setEnabled(True)
        self.btneliminar.setEnabled(False)
        self.btncancelar.setEnabled(True)

    def cancelar(self):
        self.txtcod.clear()
        self.txtrepre.clear()
        self.txtemail.clear()
        self.txtrepre.setEnabled(False)
        self.txtemail.setEnabled(False)
        self.btnnovo.setEnabled(True)
        self.btneditar.setVisible(False)
        self.btnsalvar.setEnabled(False)
        self.btnsalvar.setVisible(True)
        self.btneliminar.setEnabled(False)
        self.btncancelar.setEnabled(False)
        self.btntelrepre.setEnabled(False)

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
        self.txtrepre.setEnabled(True)
        self.txtrepre.setFocus()
        self.txtemail.setEnabled(True)
        self.btnnovo.setEnabled(False)
        self.btneditar.setVisible(False)
        self.btnsalvar.setEnabled(True)
        self.btnsalvar.setVisible(True)
        self.btneliminar.setEnabled(False)
        self.btncancelar.setEnabled(True)

    def guardar(self):
        if len(self.txtcod.text()) > 0:
            codigo = str(self.txtcod.text())
        nom = str(self.txtrepre.text())
        cod = str(self.cod)
        email = str(self.txtemail.text())
        if (len(nom) > 1):
            con = self.conexion.conectar()
            cur = con.cursor()
            if self.bnd == 0:
                cur.execute(
                    'insert into representante (nomrepre, codfornecedor, email) values(%s,%s,%s)', [nom,cod,email])
                con.commit()
                self.cancelar()
                self.consultar()
                row = self.tabla.rowCount()
                self.tabla.selectRow(row - 1)
            else:
                cur.execute('update representante set nomrepre=%s, codfornecedor=%s, email=%s where codrepre=%s', [nom, str(self.cod), email, codigo])
                con.commit()
                self.cancelar()
                self.consultar()
        else:
            mensaje = QtGui.QMessageBox.information(self, "Caracteres insuficientes",
                                                    "Um campo nao cumpre os requisitos", QtGui.QMessageBox.Ok)
            self.txtrepre.setFocus()

    def consultar(self):
        con = None
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select count(*) from representante where codfornecedor='+str(self.cod)+'and nomrepre like' + self.buscar)
        rows = cur.fetchone()

        if (int(rows[0]) > 0):
            self.lblsinreg.setVisible(False)
            self.config(rows)
            cur.execute(
                'select a.codrepre, a.nomrepre, a.email, b.nomfornecedor from representante a, fornecedor b where '
                'a.codfornecedor=b.codfornecedor and a.codfornecedor='+str(self.cod)+'and a.nomrepre like' + self.buscar + ' order by codrepre '
                                                                                         'asc')
            self.repre = cur.fetchall()

            for i in range(int(rows[0])):
                item = self.repre[i]
                cod = QtGui.QTableWidgetItem(str(item[0]))
                repre = QtGui.QTableWidgetItem(str(item[1]))
                email = QtGui.QTableWidgetItem(str(item[2]))
                fornecedor = QtGui.QTableWidgetItem(str(item[3]))
                self.tabla.setItem(i, 0, cod)
                self.tabla.setItem(i, 1, repre)
                self.tabla.setItem(i, 2, email)
                self.tabla.setItem(i, 3, fornecedor)
        else:
            self.lblsinreg.setVisible(True)
            self.tabla.setRowCount(0)
            self.tabla.setColumnCount(0)

    def cargar(self):
        self.cancelar()
        index = int(self.lblindice.text())
        item = self.repre[index]
        self.txtcod.setText(str(item[0]))
        self.txtrepre.setText(str(item[1]))
        self.txtemail.setText(str(item[2]))
        self.btnsalvar.setVisible(False)
        self.btneditar.setVisible(True)
        self.btneditar.setEnabled(True)
        self.btneliminar.setEnabled(True)
        self.btntelrepre.setEnabled(True)

    def config(self, rows):
        lista = 'Codigo', 'Representante', 'Email', 'Fornecedor'
        self.tabla.setColumnCount(4)
        self.tabla.setRowCount(int(rows[0]))
        self.tabla.setHorizontalHeaderLabels(lista)
        # self.tabla.setColumnWidth(0, 50)
        # self.tabla.setColumnWidth(1, 319)
        header = self.tabla.horizontalHeader()
        header.setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(1, QtGui.QHeaderView.Stretch)

    def eliminar(self):
        cod = int(self.txtcod.text())
        # con = None
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select count(*) from telrepre where codrepre=%s', [cod])
        rows = cur.fetchone()
        if int(rows[0]) == 0:
            mensaje = QtGui.QMessageBox.question(self, "Eliminando Registro", "Deseja Eliminar este Registro?",
                                                 QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if (mensaje == QtGui.QMessageBox.Yes):
                con = self.conexion.conectar()
                cur = con.cursor()
                cur.execute('delete from representante where codrepre = %s', [cod])
                con.commit()
                self.cancelar()
                self.consultar()
                mensaje = QtGui.QMessageBox.information(self, "Eliminando Registro", "Registro Eliminado",
                                                        QtGui.QMessageBox.Ok)
        else:
            mensaje = QtGui.QMessageBox.question(self, "Error ao eliminar registro",
                                                 "Esse registro tem uma marca registrada", QtGui.QMessageBox.Ok)

def main():
    app = QtWidgets.QApplication(sys.argv)
    form = representanteApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()