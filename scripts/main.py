# main.py
# This is the main entry point to run the entire analysis.

import time
import pandas as pd
from analysis import CovidAnalyzer
from plotting import plot_confusion_matrix
import config

def main():
    """
    Main function to execute the COVID-19 test data analysis.
    """
    print("Starting COVID-19 Analysis...")
    start_time = time.time()

    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Initialize the analyzer. It will automatically load the entity catalog.
    analyzer = CovidAnalyzer(
        filepath=config.DATA_FILE_PATH,
        entity_col=config.ENTITY_COL,
        result_lab_col=config.RESULT_LAB_COL,
        result_ant_col=config.RESULT_ANT_COL,
        final_result_col=config.FINAL_RESULT_COL,
        positive_vals=config.POSITIVE_VALUES,
        negative_val=config.NEGATIVE_VALUE
    )

    analyzer.run_analysis()
    print("Analysis complete.")

    print("\n--- National Results (Mexico) ---")
    national_report = analyzer.get_national_report()
    print(national_report)

    print("\n--- Results by Entity ---")
    entity_report = analyzer.get_entity_report()
    print(entity_report.to_string())

    # --- PLOT GENERATION ---
    print("\nSaving confusion matrix plots...")
    
    # Save the national confusion matrix plot
    national_cm_path = config.OUTPUT_DIR / "confusion_matrix_national.png"
    plot_confusion_matrix(
        analyzer.national_cm,
        labels=['Negativo', 'Positivo'],
        title="Matriz de Confusión Nacional (México)",
        filepath=national_cm_path
    )
    print(f"National matrix saved to '{national_cm_path}'")

    # Save confusion matrices for each entity using their names
    for entity_code, metrics_dict in analyzer.entity_metrics.items():
        if 'cm' in metrics_dict:
            # Get entity name from map, with a fallback for unknown codes
            entity_name = analyzer.entity_map.get(entity_code, f"Entidad_{entity_code}")
            
            # Sanitize the name to create a valid filename
            safe_filename = "".join(c for c in entity_name if c.isalnum() or c in (' ', '_')).rstrip().replace(' ', '_')
            
            entity_cm_path = config.OUTPUT_DIR / f"matriz_confusion_{safe_filename}.png"
            
            plot_confusion_matrix(
                metrics_dict['cm'],
                labels=['Negativo', 'Positivo'],
                title=f"Matriz de Confusión - {entity_name}",
                filepath=entity_cm_path
            )
    print(f"All entity matrices have been saved in '{config.OUTPUT_DIR}'")


    end_time = time.time()
    print(f"\nTotal execution time: {end_time - start_time:.2f} seconds.")


if __name__ == "__main__":
    main()
