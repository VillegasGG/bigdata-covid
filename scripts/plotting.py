# plotting.py
# Contains functions for creating and saving plots.

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import config # Import config to ensure output directory exists

def plot_confusion_matrix(cm, labels, title, filepath):
    """
    Generates and saves a styled confusion matrix plot using seaborn.

    Args:
        cm (numpy.ndarray): The confusion matrix.
        labels (list): The labels for the matrix axes ('Negative', 'Positive').
        title (str): The title for the plot.
        filepath (str or Path): The full path to save the image file.
    """
    # Ensure the output directory exists
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Increased figure width to accommodate the color bar
    plt.figure(figsize=(9, 6))
    
    # Calculate percentages for annotation, handle division by zero
    cm_sum = np.sum(cm)
    if cm_sum == 0:
        cm_perc = cm.astype(float) # Avoid error, show 0%
    else:
        cm_perc = cm / cm_sum * 100
    
    # Create annotations with counts (formatted with commas) and percentages
    annot = np.empty_like(cm).astype(str)
    rows, cols = cm.shape
    for i in range(rows):
        for j in range(cols):
            annot[i, j] = f"{cm[i, j]:,d}\n({cm_perc[i, j]:.2f}%)"

    # Create the heatmap with a professional color scheme and styling
    # cbar is now set to True to display the color scale
    ax = sns.heatmap(cm, annot=annot, fmt='', cmap='Blues',
                     xticklabels=labels, yticklabels=labels,
                     cbar=True, annot_kws={"size": 14, "weight": "bold"},
                     linewidths=.5, linecolor='black')
    
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, ha='right')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha='center')

    plt.ylabel('Etiqueta Real (Actual)', fontsize=13)
    plt.xlabel('Etiqueta Predicha (Predicted)', fontsize=13)
    plt.title(title, fontsize=16, pad=20, weight='bold')
    
    # Save the figure with a tight layout to prevent labels from being cut off
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
