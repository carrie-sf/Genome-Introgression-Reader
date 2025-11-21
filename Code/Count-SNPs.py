import pandas as pd
import numpy as np


def count_abh(csv_file_path, bin_start, bin_end):
    """
    Count 'a', 'b', 'h' characters in each column for SNPs within a POS range
    
    Parameters:
    csv_file_path (str): Path to the SNP CSV file
    bin_start: the bin starting position
    bin_end: the bin ending position
    
    Returns:
    dict: Counts of 'a', 'b', 'h' characters per column in the bin
    """
    df = pd.read_csv(csv_file_path, sep = '\t')

    
    pos_filter = (df['POS'] >= bin_start) & (df['POS'] <= bin_end)
    
    filtered_df = df[pos_filter]
    
    print(filtered_df)
    
    column_counts = {}
    
    for col in filtered_df.columns:
        counts = {'a': 0, 'b': 0, 'h': 0}
        
        for value in filtered_df[col]:
            # Convert to string and lowercase
            str_value = str(value).lower()
            counts['a'] += str_value.count('a')
            counts['b'] += str_value.count('b')
            counts['h'] += str_value.count('h')
        
        column_counts[col] = counts
    
    if not column_counts:
        print("No columns found to process")
        return None
        
    # Creating csv file
    output_data = []
    columns_list = list(column_counts.keys())
    output_data.append(columns_list)

    # Add counts for 'a', 'b', 'h' as subsequent rows
    a_counts = [column_counts[col]['a'] for col in columns_list]
    b_counts = [column_counts[col]['b'] for col in columns_list]
    h_counts = [column_counts[col]['h'] for col in columns_list]
  
    output_data.append(a_counts)
    output_data.append(b_counts)
    output_data.append(h_counts)
    
    # Create DataFrame for CSV output
    output_df = pd.DataFrame(output_data, index=['Column', 'a_count', 'b_count', 'h_count'])
    
    # Save to CSV
    output_filename = f'character_counts_{bin_start}_{bin_end}.csv'
    output_df.to_csv(output_filename, header=False)
    
    print(f"Found {len(filtered_df)} SNPs in POS range {bin_start}-{bin_end}")
    print(f"Results saved to {output_filename}")
    
    return {
        'character_counts': column_counts,
        'total_snps_in_range': len(filtered_df),
        'output_file': output_filename
    }

