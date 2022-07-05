#Developer : Akshintala Jithendra
#Date : June 1 2022
#email : a.jithendra@gmail.com


import pandas as pd
import numpy as np
import gc
from datetime import datetime
pd.options.mode.chained_assignment = None
import configparser
config = configparser.ConfigParser()
config.read("src_vs_target.config")

class ExcelComparison:
    def __init__(self):
        self.source_file = config.get('general', 'source_file')
        self.target_file = config.get('general', 'target_file')
        self.new_insert_data_file = config.get('general', 'new_insert_data_file')
        self.update_data_file = config.get('general', 'update_data_file')
        self.key_columns = config.get('general', 'key_columns')
        self.date_format_target=config.get('general', 'date_format')

    def column_comparison(self,src_df,tgt_df):
        src_cols = list(src_df.columns.values)
        tgt_cols = list(tgt_df.columns.values)
        src_cols.sort()
        tgt_cols.sort()
        if (src_cols == tgt_cols):
            return 1
        else:
            return 0
    def gen_comp_key(self,df,comp_key):
        return np.add.reduce(df[comp_key].astype(str), axis=1)

    def save_as_excel(self,filename,df):
        writer = pd.ExcelWriter(filename, engine='xlsxwriter',datetime_format=self.date_format_target)
        df.to_excel(writer, index=False)
        writer.save()

    def new_insert_data(self,src_df,comp_src_df,tgt_src_df,new_insert_data_file):
        # print(comp_src_df)
        df=comp_src_df.merge(tgt_src_df,indicator = True, how='left').loc[lambda x : x['_merge']=='left_only']
        # print(df.info())
        new_list=df['comp_key'].unique().tolist()
        del df
        gc.collect()
        # print(new_list)
        new_data_df=src_df[src_df['comp_key'].isin(new_list)]
        new_data_df['insert_datetime']=datetime.today()
        new_data_df = new_data_df.drop(['comp_key'], axis=1)
        print("Total Number Of New Rows in Source File:", new_data_df.shape[0])

        # print(new_data_df)
        self.save_as_excel(new_insert_data_file,new_data_df)
        del new_data_df
        gc.collect()
        print("New Data Excel Generated - file path:",new_insert_data_file)
        return new_list

    def update_data(self,comp_src_df,tgt_src_df,update_data_file):
        # print(comp_src_df)
        df=comp_src_df.merge(tgt_src_df,indicator = True, how='left').loc[lambda x : x['_merge']=='left_only']
        del comp_src_df,tgt_src_df
        gc.collect()
        df = df.drop(['comp_key','_merge'], axis=1)
        print("Total Number Of Rows to Update in Source File:", df.shape[0])
        df['updated_datetime'] = datetime.today()
        # print(df)
        print(df)
        self.save_as_excel(update_data_file,df)
        print("New Data Excel Generated - file path:",update_data_file)

    def comparison_process(self):
        comp_key = self.key_columns.split(",")
        src_df = pd.read_excel(self.source_file,dtype='object')
        tgt_df = pd.read_excel(self.target_file,dtype='object')
        print("Total number of rows in source file:", src_df.shape[0])
        print("Total number of rows in target file:", tgt_df.shape[0])
        col_comparison=self.column_comparison(src_df, tgt_df)
        if col_comparison==1:
            src_df['comp_key'] = self.gen_comp_key(src_df,comp_key)
            tgt_df['comp_key'] = self.gen_comp_key(tgt_df,comp_key)
            comp_src_df = src_df[['comp_key']]
            tgt_src_df = tgt_df[['comp_key']]

            ##
            new_data = self.new_insert_data(src_df,comp_src_df, tgt_src_df, self.new_insert_data_file)
            # print(src_df)
            src_df = src_df[~src_df['comp_key'].isin(new_data)]
            gc.collect()
            # print(src_df)

            self.update_data(src_df, tgt_df, self.update_data_file)
        else:
            print("No of Columns in both the files are not matching, Recheck the files. \n Caution: Columns names are case sensitive ")

if __name__ == '__main__':
    ec=ExcelComparison()
    ec.comparison_process()