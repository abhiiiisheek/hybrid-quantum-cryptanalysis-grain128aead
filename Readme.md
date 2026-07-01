# Hybrid Quantum Cryptanalysis of Grain-128AEAD using Grover's Algorithm

A hybrid quantum-classical framework for analyzing the security of the Grain-128AEAD stream cipher using Grover's search algorithm and configurable oracle selectivity.

---

## Overview

This project investigates the feasibility of quantum key recovery attacks on the Grain-128AEAD authenticated encryption algorithm.

Since constructing a fully reversible implementation of Grain-128AEAD is currently impractical for near-term quantum hardware, a hybrid cryptanalysis framework is developed that combines

- A bit-accurate classical implementation of Grain-128AEAD
- Grover's search algorithm using Qiskit
- Partial ciphertext-matching quantum oracles
- Quantum resource estimation
- Oracle selectivity analysis

The primary objective is to study how oracle strength influences amplitude amplification and the success probability of Grover's algorithm.

---

## Features

- Bit-accurate implementation of Grain-128AEAD
- Hybrid quantum-classical cryptanalysis framework
- Configurable partial-matching quantum oracle
- Grover search implementation using Qiskit
- Circuit depth and gate complexity analysis
- Oracle selectivity experiments
- Visualization of measurement distributions and amplification behavior

---

## Repository Structure

```
Hybrid_grain_grover_attack/
│
├── main.py
├── grain_classical.py
├── quantum_attack.py
├── requirements.txt
├── README.md
│
├── figures/
│   ├── histogram_7bit.png
│   ├── success_vs_bits.png
│   └── success_vs_iterations.png
│
└── docs/
    └── Hybrid_Quantum_Cryptanalysis_Grain128AEAD.pdf
```

---

## Methodology

The project consists of two components.

### Classical Component

- Implements the complete Grain-128AEAD encryption algorithm
- Generates ciphertext and authentication tag
- Produces target ciphertext bits for oracle construction

### Quantum Component

- Builds configurable Grover oracles
- Implements Grover diffusion
- Performs amplitude amplification
- Simulates measurement statistics using Qiskit Aer
- Estimates quantum circuit complexity

---

## Experimental Setup

- Cipher: Grain-128AEAD
- Key Size (simulation): 8-bit search space
- Framework: Qiskit
- Simulator: Qiskit Aer
- Shots: 4000

Oracle selectivity is evaluated using

- 5-bit matching
- 7-bit matching
- 8-bit matching

---

## Results

### Measurement Distribution (7-bit Oracle)

![Histogram](figures/histogram_7bit.png)

The oracle produces two dominant candidate states, demonstrating Grover's amplitude amplification when approximately two valid solutions exist.

---

### Success Probability vs Oracle Selectivity

![Oracle Selectivity](figures/success_vs_bits.png)

Increasing oracle selectivity significantly improves Grover's success probability by reducing the number of valid solutions.

---

### Success Probability vs Grover Iterations

![Iterations](figures/success_vs_iterations.png)

The experimental results follow the theoretical amplification behavior of Grover's algorithm.

---

## Circuit Statistics

| Metric | Value |
|---------|------:|
| Qubits | 9 |
| Circuit Depth | 122 |
| Total Gates | 546 |
| Grover Iterations | 12 |

---

## Installation

Clone the repository

```bash
git clone https://github.com/abhiiiisheek/Hybrid_grain_grover_attack.git

cd Hybrid_grain_grover_attack
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run

```bash
python main.py
```

---

## Future Work

- Fully reversible Grain-128AEAD oracle
- Reduced-round quantum cryptanalysis
- Logical qubit resource estimation
- Fault-tolerant gate count analysis
- Extension to larger key spaces

---

## Author

**Abhishek Kumar**

B.Tech Computer Science and Engineering

Indian Institute of Information Technology Kalyani

Email:
abhisheksky16112007@gmail.com

GitHub:
https://github.com/abhiiiisheek

LinkedIn:
https://linkedin.com/in/abhishek-kumar

---

## Citation

If you use this repository in your research, please cite:

```
Abhishek Kumar,
Hybrid Quantum Cryptanalysis of Grain-128AEAD using Grover's Algorithm:
An Analysis of Oracle Selectivity,
2026.
```

---

## License

This project is released under the MIT License.
