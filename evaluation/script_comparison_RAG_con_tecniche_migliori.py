#fatto a mano perché ricalcolare tutto per 3 metodi non mi andava

import matplotlib.pyplot as plt

methods = ['Docling', 'Hierarchical', 'Overlap']
values  = [0.744, 0.758, 0.882]

plt.figure(figsize=(8, 6))
bars = plt.bar(methods, values, width=0.5)

plt.title("RAG Eval - Best Accuracy Comparison", fontsize=14)
plt.ylabel("Accuracy (Corretti/Totali)")
plt.ylim(0, 1)
plt.yticks([i * 0.1 for i in range(11)])
plt.grid(True, axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()

plt.savefig("comparison-bge-3.png", dpi=150)
plt.show()
