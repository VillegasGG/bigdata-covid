# analysis.py
# Contains the core logic for analyzing the COVID-19 dataset.

import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix
import config  # Import the configuration file

class CovidAnalyzer:
    """
    A class to analyze COVID-19 test data from a large CSV file.
    It processes data in chunks to handle large files efficiently and
    calculates key performance metrics like accuracy, sensitivity, and specificity.
    """

    def __init__(self, filepath, entity_col, result_lab_col, result_ant_col,
                 final_result_col, positive_vals, negative_val):
        """
        Initializes the CovidAnalyzer.

        Args:
            filepath (str or Path): Path to the dataset CSV file.
            entity_col (str): Column name for the entity identifier.
            result_lab_col (str): Column name for lab results.
            result_ant_col (str): Column name for antigen results.
            final_result_col (str): Column name for the final classification.
            positive_vals (list): List of values indicating a positive result.
            negative_val (int): Value indicating a negative result.
        """
        self.filepath = filepath
        self.entity_col = entity_col
        self.result_lab_col = result_lab_col
        self.result_ant_col = result_ant_col
        self.final_result_col = final_result_col
        self.positive_vals = positive_vals
        self.negative_val = negative_val

        # Load the entity mapping from the catalog file
        self.entity_map = self._load_entity_map()

        self.entity_metrics = {}
        self.y_true_national = []
        self.y_pred_national = []
        self.national_cm = None

    def _load_entity_map(self):
        """Loads the entity code-to-name mapping from the Excel catalog."""
        try:
            df_catalog = pd.read_excel(
                config.CATALOG_FILE_PATH,
                sheet_name=config.CATALOG_SHEET_NAME,
                usecols=[config.CATALOG_KEY_COL, config.CATALOG_VALUE_COL]
            )
            # Create a dictionary mapping: {CLAVE_ENTIDAD: ENTIDAD_FEDERATIVA}
            # The .str.strip() removes any accidental leading/trailing whitespace
            df_catalog[config.CATALOG_VALUE_COL] = df_catalog[config.CATALOG_VALUE_COL].str.strip()
            return pd.Series(
                df_catalog[config.CATALOG_VALUE_COL].values,
                index=df_catalog[config.CATALOG_KEY_COL]
            ).to_dict()
        except FileNotFoundError:
            print(f"WARNING: Entity catalog not found at '{config.CATALOG_FILE_PATH}'.")
            print("         Reports will use entity codes instead of names.")
            return {} # Return an empty dict if file is not found
        except Exception as e:
            print(f"ERROR: Could not load entity catalog. Error: {e}")
            return {}

    def _calculate_metrics(self, cm):
        """Calculates performance metrics from a confusion matrix."""
        if cm.shape != (2, 2):
            return {
                "TP": 0, "FP": 0, "FN": 0, "VN": 0,
                "Accuracy": 0, "Sensitivity (Recall)": 0, "Specificity": 0
            }

        vn, fp, fn, tp = cm.ravel()
        
        total = tp + vn + fp + fn
        accuracy = (tp + vn) / total if total > 0 else 0
        sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
        specificity = vn / (vn + fp) if (vn + fp) > 0 else 0
        
        return {
            "TP": tp, "FP": fp, "FN": fn, "VN": vn,
            "Accuracy": accuracy,
            "Sensitivity (Recall)": sensitivity,
            "Specificity": specificity
        }

    def _process_chunk(self, chunk):
        """Processes a single chunk of the DataFrame."""
        cols_to_convert = [self.result_lab_col, self.result_ant_col, self.final_result_col]
        for col in cols_to_convert:
            chunk[col] = pd.to_numeric(chunk[col], errors='coerce')
        
        chunk.dropna(subset=cols_to_convert, inplace=True)

        for col in cols_to_convert:
            chunk[col] = chunk[col].astype(int)

        predicted_positive_mask = (chunk[self.result_lab_col] == 1) | (chunk[self.result_ant_col] == 1)
        actual_positive_mask = chunk[self.final_result_col].isin(self.positive_vals)
        
        analysis_df = chunk.copy()
        analysis_df['y_true'] = np.where(actual_positive_mask, 1, 0)
        analysis_df['y_pred'] = np.where(predicted_positive_mask, 1, 0)
        
        self.y_true_national.extend(analysis_df['y_true'])
        self.y_pred_national.extend(analysis_df['y_pred'])

        for entity, group in analysis_df.groupby(self.entity_col):
            if entity not in self.entity_metrics:
                self.entity_metrics[entity] = {'tp': 0, 'fp': 0, 'fn': 0, 'vn': 0}
            
            cm = confusion_matrix(group['y_true'], group['y_pred'], labels=[0, 1])
            vn, fp, fn, tp = cm.ravel()

            self.entity_metrics[entity]['vn'] += vn
            self.entity_metrics[entity]['fp'] += fp
            self.entity_metrics[entity]['fn'] += fn
            self.entity_metrics[entity]['tp'] += tp

    def run_analysis(self):
        """Reads the CSV file in chunks and processes them to gather metrics."""
        COLS_TO_USE = [
            self.entity_col, self.result_lab_col, self.result_ant_col, self.final_result_col
        ]
        try:
            with pd.read_csv(self.filepath, chunksize=config.CHUNK_SIZE, usecols=COLS_TO_USE, low_memory=False) as reader:
                for i, chunk in enumerate(reader):
                    print(f"  Processing chunk {i+1}...")
                    self._process_chunk(chunk)
        except FileNotFoundError:
            print(f"ERROR: The data file was not found at {self.filepath}")
            print("Please ensure the 'DATA_FILE_PATH' in config.py is correct.")
            return

        self._finalize_metrics()
        
    def _finalize_metrics(self):
        """Calculates the final confusion matrices after all chunks are processed."""
        self.national_cm = confusion_matrix(self.y_true_national, self.y_pred_national, labels=[0, 1])
        for entity_code, metrics in self.entity_metrics.items():
            self.entity_metrics[entity_code]['cm'] = np.array([
                [metrics['vn'], metrics['fp']],
                [metrics['fn'], metrics['tp']]
            ])

    def get_national_report(self):
        """Returns a formatted string of the national results."""
        if self.national_cm is None: return "Analysis has not been run yet."
        report_data = self._calculate_metrics(self.national_cm)
        return (
            f"  - True Positives (TP):  {report_data['TP']:,}\n"
            f"  - False Positives (FP): {report_data['FP']:,}\n"
            f"  - True Negatives (VN):  {report_data['VN']:,}\n"
            f"  - False Negatives (FN): {report_data['FN']:,}\n"
            f"  ----------------------------------\n"
            f"  - Accuracy:             {report_data['Accuracy']:.4f}\n"
            f"  - Sensitivity (Recall): {report_data['Sensitivity (Recall)']:.4f}\n"
            f"  - Specificity:          {report_data['Specificity']:.4f}"
        )

    def get_entity_report(self):
        """Returns a pandas DataFrame with results for each entity, using names."""
        if not self.entity_metrics: return pd.DataFrame()

        report_list = []
        for entity_code, metrics in self.entity_metrics.items():
            if 'cm' in metrics:
                entity_calcs = self._calculate_metrics(metrics['cm'])
                entity_calcs['Entity_Code'] = entity_code
                report_list.append(entity_calcs)

        report_df = pd.DataFrame(report_list)
        
        # Map the entity code to its name, keep code as a fallback
        report_df['Entidad Federativa'] = report_df['Entity_Code'].map(self.entity_map)
        report_df['Entidad Federativa'].fillna(report_df['Entity_Code'].apply(lambda x: f"Código {x}"), inplace=True)
        report_df = report_df.set_index('Entidad Federativa')
        
        cols_order = ["TP", "FP", "VN", "FN", "Accuracy", "Sensitivity (Recall)", "Specificity"]
        return report_df[cols_order]
