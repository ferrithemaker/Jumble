import biotools as bt

cadena = bt.readString("bases")

#print(cadena)
cadenaNeta = bt.limpiarCadena(cadena)

exon1 = bt.transcripcion(bt.inversa(bt.complementaria(bt.segmento(5639,5710,cadenaNeta))))
exon2 = bt.transcripcion(bt.inversa(bt.complementaria(bt.segmento(2257,2530,cadenaNeta))))
exon3 = bt.transcripcion(bt.inversa(bt.complementaria(bt.segmento(1528,2182,cadenaNeta))))
exon4 = bt.transcripcion(bt.inversa(bt.complementaria(bt.segmento(1151,1466,cadenaNeta))))
exon5 = bt.transcripcion(bt.inversa(bt.complementaria(bt.segmento(816,947,cadenaNeta))))
exon6 = bt.transcripcion(bt.inversa(bt.complementaria(bt.segmento(131,745,cadenaNeta))))

exon1 = bt.inversa(bt.complementaria(bt.segmento(5639,5710,cadenaNeta)))
exon2 = bt.inversa(bt.complementaria(bt.segmento(2257,2530,cadenaNeta)))
exon3 = bt.inversa(bt.complementaria(bt.segmento(1528,2182,cadenaNeta)))
exon4 = bt.inversa(bt.complementaria(bt.segmento(1151,1466,cadenaNeta)))
exon5 = bt.inversa(bt.complementaria(bt.segmento(816,947,cadenaNeta)))
exon6 = bt.inversa(bt.complementaria(bt.segmento(131,745,cadenaNeta)))



print(len(exon1)+len(exon2)+len(exon3)+len(exon4)+len(exon5)+len(exon6))

#print(exon1+exon2+exon3+exon4+exon5+exon6)

print(len(exon1))

print(bt.transcripcion(exon6))

print(bt.traduccion(bt.transcripcion(exon1)))
