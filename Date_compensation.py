# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 21:44:10 2023

@author: LY
"""
#%%打开某目录文件进行日期填补
import os
import numpy as np
import pandas as pd
#%%定义处理文件的函数
def compensation_date(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path)
            #原文件第一列多出了0~n的自然数列，不将其计入处理的文件中
            df = df.iloc[:,1:]
            #将日期设置为规范的日期形式
            df['dtime'] = pd.to_datetime(df['dtime'])
            
            #去除本身在python读取中引入的NAN值，记录原始文件数据的个数
            def delete_nan(sd):
                mask = np.isnan(sd)
                arr_without_nan = sd[~mask]
                return arr_without_nan
            data_num = len(delete_nan(df.iloc[:,1].values)) 

            #根据记录数据的个数计算相应的最小日期和最大日期，同时将日期转化为字符串形式方便创建日期索引，计算正常15min分钟间隔日期个数 
            #原文件最起始的日期和最终的日期
            start_date = df['dtime'][:data_num].min().strftime('%Y-%m-%d %H:%M:%S')
            end_date = df['dtime'][:data_num].max().strftime('%Y-%m-%d %H:%M:%S')   
            # 创建日期索引，每15分钟记一个数  
            date_index = pd.date_range(start=start_date, end=end_date, freq='15T')  
            # 计算正常15min分钟间隔日期个数  
            date_count = len(date_index) 
            # 为了填充日期的必要，将日期列设置为索引  
            df.set_index('dtime', inplace=True)  
            # 将日期频率调整为15分钟级别，asfreq()表示不进行前向或后向填充，fillna(0) 表示用0填充缺失值（换成其他值填充均可）  
            df = df.resample('15T').asfreq().fillna(0) 
            #去除索引，False表示不删除恢复后的日期列
            df = df.reset_index(drop=False) 
            #按照正常日期长度赋值，不计入NAN值
            df2 = df.iloc[:date_count,:]
            # 将缺失日期处理后的数据保存为新的csv文件 
            path2 = 'D:/日期填补处理后的文件夹/'
            df2.to_csv(path2+'duplicate{}'.format(filename),index=False)
           
#%%运行处理函数
compensation_date('D:/待处理的文件夹/')
