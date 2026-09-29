"""Generate architecture metric charts for GCP Healthcare API Concepts Lab (FHIR R4 Simulation). Educational synthetic metrics only."""
from pathlib import Path
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parents[1] / "docs" / "images"
OUT.mkdir(parents=True, exist_ok=True)

labels = ['Patients', 'Encounters', 'Valid', 'Invalid']
values = [40, 60, 58, 2]

fig, ax = plt.subplots(figsize=(8, 4.5))
bars = ax.bar(labels, values, color=["#4285F4", "#34A853", "#FBBC04", "#EA4335"][: len(labels)])
ax.set_title("GCP Healthcare API Concepts Lab (FHIR R4 Simulation) — Synthetic Layer Volumes (Educational)")
ax.set_ylabel("Record count (synthetic)")
for b, v in zip(bars, values):
    ax.text(b.get_x() + b.get_width() / 2, b.get_height(), str(int(v)), ha="center", va="bottom", fontsize=9)
fig.tight_layout()
fig.savefig(OUT / "layer_volumes.png", dpi=150)
plt.close()

fig2, ax2 = plt.subplots(figsize=(7, 4))
ax2.plot(labels, values, marker="o", linewidth=2, color="#1a73e8")
ax2.fill_between(range(len(labels)), values, alpha=0.15, color="#1a73e8")
ax2.set_xticks(range(len(labels)))
ax2.set_xticklabels(labels)
ax2.set_title("Processing trend (illustrative)")
ax2.set_ylabel("Rows processed")
fig2.tight_layout()
fig2.savefig(OUT / "processing_trend.png", dpi=150)
plt.close()
print(f"Wrote charts to {OUT}")
