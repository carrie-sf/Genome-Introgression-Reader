
"""
author carrie-sf

notes:
    you must import your own csv files, this file can be pulled to local
    and then run through terminal
    
    
    get_bins pulls the bin numbers from the csv file and puts them in 
    a simpler file to parse which will be saved to local
    
    
    count_abh procures the data from a bins csv files we will get when the
    program runs and goes through the snp file in each bin this counts
    a, b, and h for all returns each one as a csv per bin per
    a b and h
    
    this also returns the total count in a csv
    
"""
import pandas as pd


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
    


def count_abh(bin_output_filename, csv_file_path):
    """
    Count 'a', 'b', 'h' characters in each column for SNPs within POS ranges
    
    Parameters:
    csv_file_path (str): Path to the SNP CSV file
    bin_output_filename (str): Path to the bin positions file
    
    Returns:
    dict: Results for all bins processed
    """
    df = pd.read_csv(csv_file_path, sep='\t')
    pos = pd.read_csv(bin_output_filename, sep=',')
    pos_df = pos.drop('Bin', axis=1)
    
    all_results = {}
    
    for col in pos_df.columns:
        start = pos_df.loc[0, col]
        end = pos_df.loc[1, col]
        bin_start = int(start)
        bin_end = int(end)
        
        print(f"Processing bin {col}: {bin_start}-{bin_end}")
        
        pos_filter = (df['POS'] >= bin_start) & (df['POS'] <= bin_end)
        filtered_df = df[pos_filter]
        print(f"Found {len(filtered_df)} SNPs in this range")
        
        column_counts = {}
        for data_col in df.columns:
            counts = {'a': 0, 'b': 0, 'h': 0}
            for value in filtered_df[data_col]:
                str_value = str(value).lower()
                counts['a'] += str_value.count('a')
                counts['b'] += str_value.count('b')
                counts['h'] += str_value.count('h')
            column_counts[data_col] = counts
        
        if not column_counts:
            print(f"No columns found to process for bin {bin_start}-{bin_end}")
            continue  # Skip to next bin instead of returning
        
        # Create individual CSV files for 'a', 'b', 'h' counts and combined file
        output_files = {}
        columns_list = list(column_counts.keys())
        
        # Create individual files for each character type
        for char_type in ['a', 'b', 'h']:
            char_counts = [column_counts[col][char_type] for col in columns_list]
            
            out_df = pd.DataFrame(
                [columns_list, char_counts],
                index=['Column', f'{char_type}_count']
            )
            
            out_file = f'{char_type}_counts_{bin_start}_{bin_end}.csv'
            out_df.to_csv(out_file, header=False)
            output_files[char_type] = out_file
            print(f"{char_type.upper()} counts saved to {out_file}")

        # Create combined summary file
        combined_data = [columns_list]
        combined_data.append([column_counts[col]['a'] for col in columns_list])
        combined_data.append([column_counts[col]['b'] for col in columns_list])
        combined_data.append([column_counts[col]['h'] for col in columns_list])
        
        combined_df = pd.DataFrame(
            combined_data,
            index=['Column', 'a_count', 'b_count', 'h_count']
        )
        combined_file = f'combined_abh_counts_{bin_start}_{bin_end}.csv'
        combined_df.to_csv(combined_file, header=False)
        output_files['combined'] = combined_file
        
        print(f"Combined counts saved to {combined_file}")
        
        # Store results for this bin
        all_results[f'bin_{bin_start}_{bin_end}'] = {
            'character_counts': column_counts,
            'total_snps_in_range': len(filtered_df),
            'output_files': output_files
        }
    
    print(f"Processed {len(all_results)} bins total")
    return all_results
