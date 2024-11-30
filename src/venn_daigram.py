import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn3

# Create a Venn diagram-like structure using concentric circles
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)

# Add concentric circles
circles = [
    plt.Circle((0, 0), 1.4, color='green', alpha=0.2, label='Artificial Intelligence (AI)'),
    plt.Circle((0, 0), 1.1, color='blue', alpha=0.2, label='Machine Learning (ML)'),
    plt.Circle((0, 0), 0.8, color='blue', alpha=0.3, label='Deep Learning (DL)'),
    plt.Circle((0.2, 0), 0.4, color='orange', alpha=1, label='Generative AI'),
    plt.Circle((0.6, 0), 0.2, color='yellow', alpha=0.6, label='LLMs (Large Language Models)')
]

for circle in circles:
    ax.add_artist(circle)

# Add labels
ax.text(0, 1.2, 'Artificial Intelligence (AI)', horizontalalignment='center', fontsize=12, weight='bold')
ax.text(0, 0.9, 'Machine Learning (ML)', horizontalalignment='center', fontsize=12, weight='bold')
ax.text(0, 0.6, 'Deep Learning (DL)', horizontalalignment='center', fontsize=12, weight='bold')
ax.text(0.2, 0.2, 'Generative AI', horizontalalignment='center', fontsize=12, weight='bold', color='black')
ax.text(0.6, -0.1, 'LLMs\n(Large Language Models)', horizontalalignment='center', fontsize=12, weight='bold', color='black')

# Remove axes for clarity
ax.axis('off')

# Show the plot
plt.tight_layout()
plt.show()
# Save the diagram as a PNG file
output_path = "images/AI_Venn.png"
fig.savefig(output_path, format='png')


