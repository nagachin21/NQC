###NICT Quantum Camp 2021用コード
###サンプルプログラムnictq3-2-2.py

#必要なパッケージのインポート
import numpy as np
from qiskit import ClassicalRegister, QuantumRegister,QuantumCircuit,execute,Aer
from qiskit.tools.visualization import circuit_drawer,plot_histogram

#回路サイズの指定
qftsize = 4 #変数xのqubit数
nbits = 4 #変数yのqubit数
csize = qftsize+nbits #古典レジスタ数

xr = QuantumRegister(qftsize,'x') #4qubitの量子レジスタx
yr = QuantumRegister(nbits,'y')  #4qubitの量子レジスタy
cr = ClassicalRegister(csize,'c') #8bitの古典レジスタ

circuit = QuantumCircuit(xr,yr,cr)

###ここから量子回路の記述
#量子ゲートの記述
for i in range(qftsize):
	circuit.h(xr[i])
circuit.barrier()

#コントロール7倍
circuit.x(yr[0])
circuit.cx(xr[0],yr[1])
circuit.cx(xr[0],yr[2])
circuit.barrier()

#コントロール×4 mod 15
circuit.cswap(xr[1],yr[0],yr[2])
circuit.cswap(xr[1],yr[1],yr[3])
circuit.barrier()

#測定命令の記述
for i in range(qftsize):
	circuit.measure(xr[i],cr[i])

#a^x mod Nの計算結果確認用測定命令
for i in range(nbits):
	circuit.measure(yr[i],cr[i+qftsize])

###ここまで量子回路の記述

#シミュレーターの指定
simulator = Aer.get_backend('qasm_simulator')
#量子回路のシミュレーターを使った実行
job = execute(circuit, simulator, shots=1000)

#測定結果の取り出し
result = job.result()
counts = result.get_counts(circuit)

#測定結果のカウント表示
print("Total count [y3,y2,y1,y0,x3,x2,x1,x0]:",counts)

#10進変換追記部分
scounts = sorted(counts.items(), key=lambda x:x[0][4:8]) #xbitsの順にソート
for i in scounts:
	k=i[0]
	v=i[1]
	ybits = k[0:4]    #文字列kの0-3文字目を取り出す
	xbits = k[4:8]     #文字列kの4-7文字目を取り出す
	print('(X,Y)=',xbits,ybits,'=(',int(xbits,2),',', int(ybits,2) ,') : count=' ,v)

#測定結果のヒストグラム出力
plotgraph = plot_histogram(counts)
plotgraph.savefig("measurement.png",format="png")

#回路図のプロット
diagram = circuit.draw(output='mpl',plot_barriers=False)
diagram.savefig("circuit.png",format="png")

