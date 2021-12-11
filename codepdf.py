# -*- coding: utf-8 -*-

# Formulario que Genera PDF

 
import sys
import os
import time
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from codeconexion import conexion
from codeajuste import ajuste

class pdf():
    conexion=conexion()
    fecha=""
    hora=""
    ajustador=ajuste()
    def acthora(self):
        self.fecha=(time.strftime("%d/%m/%y"))
        self.hora=(time.strftime("%H:%M"))

    def generar(self, servi, fechamin, fechamax, bndestado, bndfecha, rows, comissao, total, cobrado):
        self.acthora()
        co=0
        #---------------------- Esta parte lee los datos del estado del proceso de servicio, Todos, Aberto 1, Processo 2, Concluido 3
        estado='Todos'
        if bndestado==1:
            estado='Abertos'
        elif bndestado==2:
            estado='Em Processo'
        elif bndestado==3:
            estado='Concluidos'
        #----------------------
        titulo='asdasd'
        if bndfecha==0:
            titulo='           Lista de Ordems de Serviço entre '+fechamin+' e '+fechamax+' '+estado
        elif bndfecha==1:
            titulo='                                   Lista de Ordems de Serviço '+estado
        #----------------------
        if rows>0:
          
            c = canvas.Canvas("ListaOrdems.pdf")
            # canvas.setPageSize(595, 842)
            # canvas.Canvas.setPageSize(landscape(A4))
            # canvas.Canvas.setPageSize(c, landscape(A4))
            renglon=690
            status=''
            for i in range(rows[0]):                
                renglon=690-co                
                if renglon<100:
                    renglon=690
                    co=0
                    c.showPage()
                if renglon==690:     
                    c.setFont("Courier",9)                    
                    c.drawString(230,780,'     Sistema "Sua Ordem"')
                    c.drawString(50,800,("Data: "+self.fecha))
                    c.drawString(480,800,("Hora: "+self.hora))
                    c.drawString(0,760,titulo)
                    c.drawString(0,740,("____________________________________________________________________________________________________________________________"))
                    c.drawString(10,720,("  Cod  N. Servi  Cliente       Equipamento         Data      Estado      Comissão      Total     Cobrado"))
                    c.drawString(0,710,("____________________________________________________________________________________________________________________________"))
                item=servi[i]
                # O primeiro item é o dato e o segundo o numero de espaços maximo no campo de texto
                # Ajustarstr coloca espaço pra direita e ajustarnum pra esquerda
                cod=self.ajustador.ajustarnum(str(item[0]),5)
                # servi=self.ajustador.ajustarnum(str('%.2f' %(float(item[5]))),7)
                serv=self.ajustador.ajustarstr(str(item[1]),8)
                cliente=self.ajustador.ajustarstr(str(item[2]).decode('utf8'),12)
                # funcio=self.ajustador.ajustarstr(str(item[3]),7)
                equip=self.ajustador.ajustarstr(str(item[4]).decode('utf8'),16)
                data=self.ajustador.ajustarstr(str(item[5]),10)
                #guioncero=self.ajustador.ajustarstr("------------------------------",9)
                # Conversor de estado
                if int(item[6]) == 1:
                    status = 'Aberto'
                elif int(item[6]) == 2:
                    status = 'Em processo'
                elif int(item[6]) == 3:
                    status = 'Concluido'
                status=self.ajustador.ajustarstr(str(status),11)
                comissaocero=self.ajustador.ajustarnum(str(item[7]),8)
                totalcero=self.ajustador.ajustarnum(str(item[8]),9)
                cobradocero=self.ajustador.ajustarnum(str(item[9]),9)
                co=co+20
                c.drawString(0,renglon,('  '+cod+"  "+serv+"  "+cliente+"  "+equip+" "+data+"   "+status+" "+comissaocero+"  "+totalcero+"   "+cobradocero))
            comissao=self.ajustador.ajustarnum(str('%.2f' %float(comissao)),8)
            total=self.ajustador.ajustarnum(str('%.2f' %float(total)),9)
            cobrado=self.ajustador.ajustarnum(str('%.2f' %float(cobrado)),9)
            c.drawString(0,renglon-20,("____________________________________________________________________________________________________________________________"))
            c.drawString(11,renglon-35,("  Total:                                                                 "+comissao+'  '+total+'   '+cobrado))
            c.drawString(0,renglon-40,("____________________________________________________________________________________________________________________________"))
            renglon=690-co  
            if renglon<40:
                renglon=690
                co=0
                c.showPage()
            if renglon==690:     
                c.setFont("Courier",9)
                c.drawString(230, 780, '     Sistema "Sua Ordem"')
                c.drawString(50,800,("Data: "+self.fecha))
                c.drawString(480,800,("Hora: "+self.hora))
                c.drawString(0,760,(titulo))
                c.drawString(0,740,("____________________________________________________________________________________________________________________________"))
                # c.drawString(10,720,("        Data        Valor      Conta      N° Cheque     Agencia      Banco           Loja        Pagado"))
                c.drawString(0,710,("____________________________________________________________________________________________________________________________"))
            
            
            c.save()
            os.system("start ListaOrdems.pdf &")
      
        
if __name__ == "__main__":
    MyWindow = pdf()
    # MyWindow.generar('01/02/2016','22/02/2017')
       