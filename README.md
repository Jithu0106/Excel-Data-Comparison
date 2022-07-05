### Developer : Akshintala Jithendra
### Date : June 1 2022

## Excel-Data-Comparison

Compare data between two excels and result new and modified rows into new excel as output

## Usage : 

 Update the src_vs_tgt.config file to configure source file and target file which you want to provide as input under [general] section.

## Config Parameters :

source_file -> provide source excel file path including file name

target_file -> provide target excel file path including file name

new_insert_data_file -> Provide excel file path to get new records from source file after comparing with target file

update_data_file -> Provide excel file path to get modified records from source file after comparing with target file

key_columns -> provide one or more columns to generate unique key

date_format -> provide a date format so that while writing the output data to excel all datetime columns will use the same format

## Example configuration : 

source_file=/home/jithendra/Downloads/src_test_data.xlsx

target_file=/home/jithendra/Downloads/tgt_test_data.xlsx

new_insert_data_file=/home/jithendra/Downloads/new_insert_data.xlsx

update_data_file=/home/jithendra/Downloads/update_data.xlsx

key_columns=ID,Code

date_format=mmm d, yyyy

Run src_vs_target_excel_comparison.py to get the output of new and modified records 
