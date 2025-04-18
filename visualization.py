import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.patches as mpatches

def visualize_memory(manager):
    """Displays memory allocation with process labels & a properly positioned legend."""
    memory_state = manager.get_memory_state()

    # Unique process IDs mapped to colors
    unique_ids = sorted(set(p for p in memory_state if p != "Free"))
    id_mapping = {pid: i + 1 for i, pid in enumerate(unique_ids)}

    # Convert memory state to numbers (Free -> 0, Processes -> Unique IDs)
    numeric_memory = [id_mapping.get(p, 0) for p in memory_state]

    plt.figure(figsize=(12, 5))  # Adjusted size for better fit
    data = np.array(numeric_memory).reshape(1, len(numeric_memory))
    
    ax = sns.heatmap(data, annot=False, fmt="d", cmap="coolwarm", cbar=False, linewidths=0.5)

    ax.set_title("📊 Memory Allocation & Segmentation", fontsize=14, fontweight="bold")
    ax.set_xlabel("Memory Blocks", fontsize=12)
    ax.set_ylabel("Allocation Status", fontsize=12)

    # Adding process labels inside heatmap
    for i, p in enumerate(memory_state):
        if p != "Free":
            ax.text(i + 0.5, 0.5, p, ha="center", va="center", fontsize=8, color="white", fontweight="bold")

    # Creating a dynamic legend
    legend_patches = [
        mpatches.Patch(color=sns.color_palette("coolwarm", len(unique_ids))[i], label=f"Process {pid}") 
        for i, pid in enumerate(unique_ids)
    ]

    # Fix: Explicitly adding legend to the figure
    legend = plt.legend(handles=legend_patches, title="Process Legend", loc="upper right",
                        bbox_to_anchor=(1, 1), fontsize=10, frameon=True)
    
    plt.gca().add_artist(legend)  # Ensure legend is drawn

    plt.xticks([])
    plt.yticks([])

    plt.show()
 
