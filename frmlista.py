# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmlista.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_frmlista(object):
    def setupUi(self, frmlista):
        frmlista.setObjectName("frmlista")
        frmlista.resize(1120, 580)
        self.groupBox = QtWidgets.QGroupBox(frmlista)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 1101, 561))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.tabla = QtWidgets.QTableWidget(self.groupBox)
        self.tabla.setGeometry(QtCore.QRect(10, 40, 1081, 471))
        self.tabla.setLocale(QtCore.QLocale(QtCore.QLocale.Portuguese, QtCore.QLocale.Brazil))
        self.tabla.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tabla.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tabla.setObjectName("tabla")
        self.tabla.setColumnCount(0)
        self.tabla.setRowCount(0)
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.verticalHeader().setHighlightSections(True)
        self.cboestado = QtWidgets.QComboBox(self.groupBox)
        self.cboestado.setGeometry(QtCore.QRect(610, 10, 101, 22))
        self.cboestado.setLocale(QtCore.QLocale(QtCore.QLocale.Portuguese, QtCore.QLocale.Brazil))
        self.cboestado.setObjectName("cboestado")
        self.cboestado.addItem("")
        self.cboestado.addItem("")
        self.cboestado.addItem("")
        self.cboestado.addItem("")
        self.datemin = QtWidgets.QDateEdit(self.groupBox)
        self.datemin.setEnabled(False)
        self.datemin.setGeometry(QtCore.QRect(290, 10, 110, 22))
        self.datemin.setLocale(QtCore.QLocale(QtCore.QLocale.Portuguese, QtCore.QLocale.Brazil))
        self.datemin.setCalendarPopup(True)
        self.datemin.setObjectName("datemin")
        self.datemax = QtWidgets.QDateEdit(self.groupBox)
        self.datemax.setEnabled(False)
        self.datemax.setGeometry(QtCore.QRect(440, 10, 110, 22))
        self.datemax.setLocale(QtCore.QLocale(QtCore.QLocale.Portuguese, QtCore.QLocale.Brazil))
        self.datemax.setCalendarPopup(True)
        self.datemax.setDate(QtCore.QDate(2020, 1, 1))
        self.datemax.setObjectName("datemax")
        self.checkdata = QtWidgets.QCheckBox(self.groupBox)
        self.checkdata.setGeometry(QtCore.QRect(240, 10, 51, 21))
        self.checkdata.setObjectName("checkdata")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(560, 10, 46, 20))
        self.label.setObjectName("label")
        self.lblsinreg = QtWidgets.QLabel(self.groupBox)
        self.lblsinreg.setGeometry(QtCore.QRect(460, 260, 81, 16))
        self.lblsinreg.setObjectName("lblsinreg")
        self.txtbuscar = QtWidgets.QLineEdit(self.groupBox)
        self.txtbuscar.setGeometry(QtCore.QRect(82, 10, 151, 20))
        self.txtbuscar.setLocale(QtCore.QLocale(QtCore.QLocale.Portuguese, QtCore.QLocale.Brazil))
        self.txtbuscar.setObjectName("txtbuscar")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 71, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(410, 10, 21, 21))
        self.label_3.setObjectName("label_3")
        self.btnimprimir = QtWidgets.QPushButton(self.groupBox)
        self.btnimprimir.setGeometry(QtCore.QRect(1020, 10, 75, 21))
        self.btnimprimir.setObjectName("btnimprimir")
        self.cbofuncio = QtWidgets.QComboBox(self.groupBox)
        self.cbofuncio.setGeometry(QtCore.QRect(820, 10, 191, 21))
        self.cbofuncio.setLocale(QtCore.QLocale(QtCore.QLocale.Portuguese, QtCore.QLocale.Brazil))
        self.cbofuncio.setObjectName("cbofuncio")
        self.lblindice = QtWidgets.QLabel(self.groupBox)
        self.lblindice.setGeometry(QtCore.QRect(260, 60, 46, 13))
        self.lblindice.setObjectName("lblindice")
        self.checkfuncio = QtWidgets.QCheckBox(self.groupBox)
        self.checkfuncio.setGeometry(QtCore.QRect(730, 10, 91, 21))
        self.checkfuncio.setObjectName("checkfuncio")
        self.totalcobrado = QtWidgets.QLineEdit(self.groupBox)
        self.totalcobrado.setGeometry(QtCore.QRect(962, 520, 131, 31))
        self.totalcobrado.setReadOnly(True)
        self.totalcobrado.setObjectName("totalcobrado")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(870, 520, 91, 31))
        self.label_4.setObjectName("label_4")
        self.total = QtWidgets.QLineEdit(self.groupBox)
        self.total.setGeometry(QtCore.QRect(730, 520, 131, 31))
        self.total.setText("")
        self.total.setReadOnly(True)
        self.total.setObjectName("total")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(690, 520, 41, 31))
        self.label_5.setObjectName("label_5")
        self.totalcomissao = QtWidgets.QLineEdit(self.groupBox)
        self.totalcomissao.setGeometry(QtCore.QRect(540, 520, 141, 31))
        self.totalcomissao.setReadOnly(True)
        self.totalcomissao.setObjectName("totalcomissao")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(440, 520, 101, 31))
        self.label_6.setObjectName("label_6")
        self.lblindice.raise_()
        self.tabla.raise_()
        self.cboestado.raise_()
        self.datemin.raise_()
        self.datemax.raise_()
        self.checkdata.raise_()
        self.label.raise_()
        self.lblsinreg.raise_()
        self.txtbuscar.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.btnimprimir.raise_()
        self.cbofuncio.raise_()
        self.checkfuncio.raise_()
        self.totalcobrado.raise_()
        self.label_4.raise_()
        self.total.raise_()
        self.label_5.raise_()
        self.totalcomissao.raise_()
        self.label_6.raise_()

        self.retranslateUi(frmlista)
        self.tabla.cellClicked['int','int'].connect(self.lblindice.setNum) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(frmlista)
        frmlista.setTabOrder(self.txtbuscar, self.checkdata)
        frmlista.setTabOrder(self.checkdata, self.datemin)
        frmlista.setTabOrder(self.datemin, self.datemax)
        frmlista.setTabOrder(self.datemax, self.cboestado)
        frmlista.setTabOrder(self.cboestado, self.tabla)

    def retranslateUi(self, frmlista):
        _translate = QtCore.QCoreApplication.translate
        frmlista.setWindowTitle(_translate("frmlista", "Lista de ordems de serviço"))
        self.cboestado.setItemText(0, _translate("frmlista", "Todos"))
        self.cboestado.setItemText(1, _translate("frmlista", "Aberto"))
        self.cboestado.setItemText(2, _translate("frmlista", "Em processo"))
        self.cboestado.setItemText(3, _translate("frmlista", "Concluido"))
        self.checkdata.setText(_translate("frmlista", "Data"))
        self.label.setText(_translate("frmlista", "Estado:"))
        self.lblsinreg.setText(_translate("frmlista", "Sem Registros"))
        self.label_2.setText(_translate("frmlista", "Nro. Ordem:"))
        self.label_3.setText(_translate("frmlista", "até"))
        self.btnimprimir.setText(_translate("frmlista", "Imprimir"))
        self.lblindice.setText(_translate("frmlista", "TextLabel"))
        self.checkfuncio.setText(_translate("frmlista", "Funcionario"))
        self.label_4.setText(_translate("frmlista", "TOTAL COBRADO:"))
        self.label_5.setText(_translate("frmlista", "TOTAL:"))
        self.label_6.setText(_translate("frmlista", "TOTAL COMISSÃO:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    frmlista = QtWidgets.QWidget()
    ui = Ui_frmlista()
    ui.setupUi(frmlista)
    frmlista.show()
    sys.exit(app.exec_())