###NICT Quantum Camp 2021用コード
###サンプルプログラムnictq3-3-1.py

import numpy as np
from qiskit import ClassicalRegister, QuantumRegister
from qiskit.tools.visualization import circuit_drawer
from qiskit.compiler import transpile
from qiskit import(
  QuantumCircuit,
  execute,
  Aer)
from qiskit.visualization import plot_histogram

######################
#QFT†サブルーチン over qreg[0,...,m-1] 
def generaliqft(circuit,qreg,m):
	for j in range (m-1,-1,-1):  #j=m-1,…,0
		for k in range (m-1,j,-1):   #k=m-1,…,j+1
			circuit.cp(-np.pi/(2**(k-j)),qreg[k],qreg[j])
		circuit.h(qreg[j])
		circuit.barrier()
######################

#回路サイズの指定
qftsize = 4 #変数xのqubit数
nbits = 4 #変数yのqubit数
csize = qftsize #古典レジスタ数（測定はQFTdagの出力）

xr = QuantumRegister(qftsize,'x') #4qubitの量子レジスタx
yr = QuantumRegister(nbits,'y')  #4qubitの量子レジスタy
cr = ClassicalRegister(csize,'c') #4bitの古典レジスタ

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

#QFT†
generaliqft(circuit,xr,qftsize)
circuit.barrier()

#測定命令の記述
for i in range(qftsize):
	circuit.measure(xr[i],cr[i])
###ここまで量子回路の記述

#シミュレーターの指定
simulator = Aer.get_backend('qasm_simulator')
#量子回路のシミュレーターを使った実行
job = execute(circuit, simulator, shots=1000)

#測定結果の取り出し
result = job.result()
counts = result.get_counts(circuit)


#測定結果のカウント表示
print("Total count [x3,x2,x1,x0]:",counts)

plotgraph = plot_histogram(counts)
plotgraph.savefig("measurement.png",format="png")

style = {'figwidth': 15}
diagram = circuit.draw(output='mpl',plot_barriers=False,fold=50,style=style)
diagram.savefig("circuit.png",format="png")

