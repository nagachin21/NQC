
import numpy as np
from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit, execute, Aer
from qiskit.tools.visualization import circuit_drawer,plot_histogram

#回路サイズの指定
qr = QuantumRegister(3,'q') #3qubitの量子レジスタ
circuit = QuantumCircuit(qr,cr)

###ここから量子回路の記述
#量子ゲートの記述
circuit.h(qr[0])
circuit.cx(qr[0],qr[1])
circuit.ccx(qr[0],qr[1],qr[2]) #circuit.cx(qr[0],qr[2])

#測定命令の記述
circuit.measure(qr[0],cr[0])
circuit.measure(qr[1],cr[1])
circuit.measure(qr[2],cr[2])
###ここまで量子回路の記述

#シミュレーターの指定
simulator = Aer.get_backend('qasm_simulator')
#量子回路のシミュレーターを使った実行
job = execute(circuit, simulator, shots=1000)

#測定結果の取り出し
result = job.result()
counts = result.get_counts(circuit)

#測定結果のカウント表示
print("Total count [q2,q1,q0]:",counts)

#測定結果のヒストグラム出力
plotgraph = plot_histogram(counts)
plotgraph.savefig("measurement.png",format="png")

#回路図のプロット
diagram = circuit.draw(output='mpl')
diagram.savefig("circuit.png",format="png")

