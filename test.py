#!/usr/bin/python
# -*- coding: latin-1 -*-
num = '123.123'
res = ''
bandera = 0
res2 = ''
try:
    float(num)
except:
    bandera = 1
# # Cambiar punto por coma y coma por punto si así se quiere
# if bandera != 1:
#     # Inserción de comas separadoras de centenas
#     if len(num)>3:
#         tam = len(num)
#         for i in range (len(num)):
#             if (tam%3)==0:
#                 if tam == len(num):
#                     res = res + num[i]
#                 else:
#                     res = res + '.' + num[i]
#             else:
#                 res = res + num[i]
#             tam = tam - 1
#             print res
#
#     # Cambiador de punto a coma
#     for i in range(len(res)):
#         if res[i] == ".":
#             res2 = res2 + ","
#         else:
#             res2 = res2 + res[i]
#
#     print res2 + ' Success'
# else:
#     print 'Error'


# Cambiar punto por coma y coma por punto si así se quiere
if bandera != 1:
    # Inserción de comas separadoras de centenas
    if len(num)>3:
        tam = len(num)
        for i in range(len(num)):
            if num[i]!='.':
                if (tam%3)==0:
                    if tam == len(num):
                        res = res + num[i]
                    else:
                        res = res + '.' + num[i]
                else:
                    res = res + num[i]
                tam = tam - 1
                print res
            else:
                res = res + ','

    # Cambiador de punto a coma
    for i in range(len(res)):
        if res[i] == ".":
            res2 = res2 + ","
        else:
            res2 = res2 + res[i]

    print res2 + ' Success'
else:
    print 'Error'

