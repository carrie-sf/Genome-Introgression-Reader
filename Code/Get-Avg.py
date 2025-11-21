import pandas as pd
import numpy as np


def average(csv_file_path, chromosome, bin_class):
    """
    Count 'a', 'b', 'h' characters in each column for SNPs within a POS range
    
    Parameters:
    csv_file_path (str): Path to the SNP CSV file
    chromosome: just for naming file
    bin_class: just for naming file
    
    Returns:
    dict: average of 'a', 'b', 'h' SNPs per bin average of all a/b/h over reps
    """
    df = pd.read_csv(csv_file_path, sep = ',')
            
    df['Average'] = df.iloc[:, 5:].mean(axis=1)

    cols = ['Average'] + [col for col in df.columns if col != 'Average']
    df = df[cols]
    
    filename = f'{chromosome}_{bin_class}.csv'
    df.to_csv(filename, index=False)
    
    print(f"Results saved to {filename}")
    
