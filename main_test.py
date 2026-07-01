from grain_classical import Grain128AEADv2
from quantum_attack import run_quantum_attack
from collections import Counter
from quantum_attack import run_quantum_attack, analyze_circuit

key   = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
nonce = bytes.fromhex("000102030405060708090a0b")
ad    = bytes.fromhex("0001020304050607")
pt    = bytes.fromhex("0001020304050607")

grain = Grain128AEADv2(key, nonce)
ct, tag = grain.encrypt(ad, pt)

print("CT :", ct.hex())
print("TAG:", tag.hex())

# Extract target bits
first_byte = ct[0]
target_bits = [int(x) for x in bin(first_byte)[2:].zfill(8)[:7]]

print("Target bits:", target_bits)

qc, counts = run_quantum_attack(target_bits)

print("Results:", counts)

analyze_circuit(qc)
