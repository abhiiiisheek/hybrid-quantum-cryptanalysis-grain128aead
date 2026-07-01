import matplotlib.pyplot as plt

data = [
    {"bits": 5, "shots": 1024, "max_count": 17},
    {"bits": 5, "shots": 4000, "max_count": 141},
    {"bits": 7, "shots": 4000, "max_count": 1301},
    {"bits": 8, "shots": 4000, "max_count": 4000}
]

bits = [d["bits"] for d in data]
success_prob = [d["max_count"] / d["shots"] for d in data]

plt.figure()
plt.plot(bits, success_prob, marker='o')
plt.xlabel("Number of Matching Output Bits (Oracle Selectivity)")
plt.ylabel("Success Probability")
plt.title("Success Probability vs Oracle Selectivity")
plt.grid()
plt.savefig("success_vs_bits.png")
plt.show()
#plt.yscale('log')

results_7bit = {
    '11101001': 1301,
    '01101001': 1262,
    '01001001': 169,
    '10001001': 149,
    '00101001': 145,
    '00001001': 138,
    '11001001': 169
}

# take top states
sorted_results = sorted(results_7bit.items(), key=lambda x: x[1], reverse=True)[:10]

states = [x[0] for x in sorted_results]
counts = [x[1] for x in sorted_results]

plt.figure(figsize=(8,5))
plt.bar(states, counts)
plt.xlabel("States")
plt.ylabel("Counts")
plt.title("Measurement Distribution under 7-bit Oracle")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("histogram_7bit.png")
plt.show()

iterations = [3, 10, 12]
success = [0.02, 0.3, 1.0]

plt.figure()
plt.plot(iterations, success, marker='o')
plt.xlabel("Grover Iterations")
plt.ylabel("Success Probability")
plt.title("Success Probability vs Grover Iterations")
plt.grid()
plt.savefig("success_vs_iterations.png")
plt.show()
