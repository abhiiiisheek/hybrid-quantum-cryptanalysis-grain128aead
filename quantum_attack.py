from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit import transpile
from collections import Counter

def grain_oracle(qc, key_qubits, target_bits, oracle_qubit):
    """
    Marks states where key_qubits match target_bits
    """

    # Flip qubits where target bit = 0
    for i, bit in enumerate(target_bits):
        if bit == 0:
            qc.x(key_qubits[i])

    # Multi-controlled X (phase flip)
    qc.mcx(key_qubits[:len(target_bits)], oracle_qubit)

    # Undo flips
    for i, bit in enumerate(target_bits):
        if bit == 0:
            qc.x(key_qubits[i])


def diffusion(qc, qubits):
    """
    Standard Grover diffusion operator
    """

    # H + X
    for q in qubits:
        qc.h(q)
        qc.x(q)

    # Multi-controlled Z
    qc.h(qubits[-1])
    qc.mcx(qubits[:-1], qubits[-1])
    qc.h(qubits[-1])

    # X + H
    for q in qubits:
        qc.x(q)
        qc.h(q)

def run_quantum_attack(target_bits, shots=4000):

    n = 8 
    qc = QuantumCircuit(n + 1, n) 

    key_qubits = list(range(n))
    oracle = n

  
    for q in key_qubits:
        qc.h(q)

    # Oracle qubit |-> state
    qc.x(oracle)
    qc.h(oracle)


    iterations = 12 

    for _ in range(iterations):
        grain_oracle(qc, key_qubits, target_bits, oracle)
        diffusion(qc, key_qubits)

    qc.measure(key_qubits, range(n))

    sim = AerSimulator()
    compiled = transpile(qc, sim)
    result = sim.run(compiled, shots=shots).result()

    counts = result.get_counts()

    return qc, counts


def analyze_circuit(qc):

    print("\n===== CIRCUIT ANALYSIS =====")

    # Basic metrics
    print("Qubits:", qc.num_qubits)
    print("Depth :", qc.depth())
    print("Total gates:", qc.size())

    # Gate counts
    gate_counts = Counter([inst.operation.name for inst in qc.data])

    print("\nGate Counts:")
    for gate, count in gate_counts.items():
        print(f"{gate}: {count}")

    # Toffoli count
    toffoli = gate_counts.get("ccx", 0)
    print("\nToffoli gates:", toffoli)

    # T-count estimation
    T_count = 7 * toffoli
    print("Estimated T-count:", T_count)

    total_T_cost = 2 * T_count * grover_iterations
    print("Estimated total T-cost:", total_T_cost)

