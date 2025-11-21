#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 11 15:27:24 2025

@author: carolinelee

this code is to extract the bin numbers from the bin csv
plug those bin numbers into the count abh to extract from snp csv
export files as a b and h counts per rep, separate by a b and h
"""

import pandas as pd

global bin_start
global bin_end

#bins

def get_bins(csv_file_path, bin_number):
    """
    Pull bin start and end from original bin csv
    returns bin start and end to be used in count_abh
    
    Parameters:
    csv_file_path (str): Path to the bins CSV file
    bin_number: the number of bins
    
    Returns:
    variables of bin_start and bin_end in csv file... not sure how to 
    """
    #df = pd.read_csv(csv_file_path, sep = ',')
    df = pd.read_csv(csv_file_path, sep = ',', nrows=2)
    df_bins = df.drop('##binmap id', axis=1)
    column_counts = {}
    
    
    for col in df_bins.columns:
       # Assuming first row has start values, second row has end values
       start = df_bins.loc[0, col]
       end = df_bins.loc[1, col]  # Changed to row 1 for end values
       column_counts[col] = {'start': start, 'end': end}
   
    if not column_counts:
        print("No columns found to process")
        return None
    
    #creating csv
    output_data = []
    columns_list = list(column_counts.keys())
    output_data.append(columns_list)

    # Add counts for 'a', 'b', 'h' as subsequent rows
    bin_start = [column_counts[col]['start'] for col in columns_list]
    bin_end = [column_counts[col]['end'] for col in columns_list]

    output_data.append(bin_start)
    output_data.append(bin_end)
    
    # Create DataFrame for CSV output
    output_df = pd.DataFrame(output_data, index=['Bin', 'bin_start', 'bin_end'])
    
    # Save to CSV
    bin_output_filename = f'bin_positions_for_{bin_number}.csv'
    output_df.to_csv(bin_output_filename, header=False)
    
    return (bin_output_filename)
    print(f"Results saved to {bin_output_filename}")
    

    
    
