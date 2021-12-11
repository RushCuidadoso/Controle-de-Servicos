from PyQt5 import QtGui, QtCore, QtWidgets
import sys
import psycopg2
import frmmedida
from codeconexion import conexion

class medidaApp(QtWidgets.QMainWindow, frmmedida.Ui_frmmedida):
    conexion = conexion()
    # caller = None
    buscar="'%%'"
    entertabla=0
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)    
        #self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.bnd=0
        self.consultar()
        self.cancelar()
        #self.setFixedWidth(830)
        #self.setFixedHeight(260)
        self.txtbuscar.textChanged.connect(self.fbuscar)          
        self.btnnovo.clicked.connect(self.nuevo)
        self.btncancelar.clicked.connect(self.cancelar)
        self.tabla.cellDoubleClicked.connect(self.devolver)
        self.tabla.cellClicked.connect(self.cargar)
        self.btneditar.clicked.connect(self.editar)
        self.btnsalvar.clicked.connect(self.guardar)
        self.lblindice.setVisible(False)
        self.btneliminar.clicked.connect(self.eliminar)
        #self.lblindice.setVisible(False)
        #-----
        #self.tabla.setSortingEnabled(True)
        #self.tabla.resizeRowsToContents()
        #self.tabla.horizontalHeader().sortIndicatorChanged.connect(self.tabla.resizeRowsToContents)    
        
        #header = self.tabla.horizontalHeader()
        #header.setStretchLastSection(True)                
        #-----        
        #self.cargarbanco()
        self.txtnom.returnPressed.connect(self.toabreviatura)
        self.txtabreviatura.returnPressed.connect(self.tobtnsalvar)
        self.btnsalvar.setAutoDefault(True)
        self.txtbuscar.returnPressed.connect(self.totabla)
        self.tabla.itemSelectionChanged.connect(self.cargar)

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

    def toabreviatura(self):
        self.txtabreviatura.setFocus()

    def tobtnsalvar(self):
        self.btnsalvar.setFocus()

    def closeEvent(self, *args, **kwargs):
        self.caller.setEnabled(True)
        # self.caller.txtcodmedida.setFocus()
        
    def iniciar(self,caller,estado):
        self.caller=caller
        self.estado=estado
        #self.cerrar=0        
        
    def devolver(self):
        #para marca, estado 1
        #para medida, estado 2
        #colocar tambem no codeproducto
        if self.estado==2:
            #item=self.marca[int(self.lblindice.text())]            
            self.caller.consultarmedida(str(self.txtcod.text()))
            self.caller.setEnabled(True)
            self.close()        
        
    def nuevo(self):
        #al clicar en el boton se prepara para guardar una informacion
        self.cancelar()
        self.bnd=0
        self.txtnom.setEnabled(True)
        self.txtnom.setFocus()
        self.txtabreviatura.setEnabled(True)
        self.btnnovo.setEnabled(False)
        self.btneditar.setVisible(False)
        self.btneditar.setEnabled(False)
        self.btnsalvar.setVisible(True)
        self.btnsalvar.setEnabled(True)
        self.btneliminar.setEnabled(False)
        self.btncancelar.setEnabled(True)
        
    def cancelar(self):
        self.txtnom.setEnabled(False)
        self.txtabreviatura.setEnabled(False)
        self.txtnom.clear()
        self.txtcod.clear()
        self.txtabreviatura.clear()
        self.btnnovo.setEnabled(True)
        self.btneditar.setVisible(False)
        self.btnsalvar.setEnabled(False)
        self.btnsalvar.setVisible(True)
        self.btneliminar.setEnabled(False)
        self.btncancelar.setEnabled(False)
        self.entertabla=0
        
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
        self.txtabreviatura.setEnabled(True)
        self.txtnom.setEnabled(True)
        self.txtnom.setFocus()
        self.btnnovo.setEnabled(False)
        self.btneditar.setVisible(False)
        self.btnsalvar.setEnabled(True)
        self.btnsalvar.setVisible(True)
        self.btneliminar.setEnabled(False)
        self.btncancelar.setEnabled(True)    
        
    def guardar(self):
        if len(self.txtcod.text()) > 0:
            cod = str(self.txtcod.text())
        nom = str(self.txtnom.text())
        abreviatura = str(self.txtabreviatura.text())
        if (len(nom) > 1) and (len(abreviatura) >=1):
            con = self.conexion.conectar()
            cur = con.cursor()
            if self.bnd == 0:
                cur.execute(
                    'insert into medida (nommedida,abreviatura) values(%s,%s)',[nom,abreviatura])    
                con.commit()                
                self.cancelar()
                self.consultar()                
                row=self.tabla.rowCount()
                self.tabla.selectRow(row-1)                
            else:
                cur.execute('update medida set nommedida=%s, abreviatura=%s where codmedida=%s',[nom, abreviatura, cod])
                con.commit()
                self.cancelar()
                self.consultar()
        else:
            mensaje = QtGui.QMessageBox.information(self, "Caracteres insuficientes","Um campo nao cumpre os requisitos", QtGui.QMessageBox.Ok) 
            
    def eliminar(self):
        cod = int(self.txtcod.text())
        #con = None
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select count(*) from produto where codmedida=%s',[cod])
        rows = cur.fetchone()
        if int(rows[0])==0:
            mensaje = QtGui.QMessageBox.question(self, "Eliminando Registro", "Deseja Eliminar este Registro?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if (mensaje == QtGui.QMessageBox.Yes):
                con = self.conexion.conectar()
                cur = con.cursor()
                cur.execute('delete from medida where codmedida = %s', [cod])
                con.commit()
                self.cancelar()
                self.consultar()
                mensaje = QtGui.QMessageBox.information(self, "Eliminando Registro", "Registro Eliminado", QtGui.QMessageBox.Ok)
        else:
            mensaje = QtGui.QMessageBox.question(self, "Error ao eliminar registro", "Esse registro tem um produto registrado",QtGui.QMessageBox.Ok)    
            
    def config(self,rows):
        lista = 'Codigo', 'Medida', 'Abreviatura'
        self.tabla.setColumnCount(3)
        self.tabla.setRowCount(int(rows[0]))
        self.tabla.setHorizontalHeaderLabels(lista)   
        #self.tabla.setColumnWidth(0,50)
        self.tabla.setColumnWidth(1,250) 
        header = self.tabla.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        
    def consultar(self):
        con = None
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select count(*) from medida where nommedida like' + self.buscar)
        rows = cur.fetchone()
        
        if (int(rows[0]) > 0):
            self.lblsinreg.setVisible(False)
            self.config(rows)
            cur.execute('select codmedida, nommedida, abreviatura from medida where nommedida like' + self.buscar + ' order by codmedida asc')
            self.marca = cur.fetchall()

            for i in range(int(rows[0])):
                item = self.marca[i]
                cod = QtWidgets.QTableWidgetItem(str(item[0]))
                marca = QtWidgets.QTableWidgetItem(str(item[1]))
                medida = QtWidgets.QTableWidgetItem(str(item[2]))
                self.tabla.setItem(i, 0, cod)
                self.tabla.setItem(i, 1, marca)
                self.tabla.setItem(i, 2, medida)
        else:
            self.lblsinreg.setVisible(True)
            self.tabla.setRowCount(0)
            self.tabla.setColumnCount(0)
            
    def cargar(self):
        self.cancelar()
        # index = int(self.lblindice.text())
        index = self.tabla.currentRow()
        item = self.marca[index]
        self.txtcod.setText(str(item[0]))
        self.txtnom.setText(str(item[1]))
        self.txtabreviatura.setText(str(item[2]))
        self.btnsalvar.setVisible(False)
        self.btneditar.setVisible(True)
        self.btneditar.setEnabled(True)
        self.btneliminar.setEnabled(True)  
        
def main():
    app = QtWidgets.QApplication(sys.argv)
    form = medidaApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()