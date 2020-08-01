# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 12:03:02 2020

@author: cbian
"""

import os
import pandas as pd
import itertools
import collections
import csv

dict_real_sa = {}
dict_real_da = {}
dict_gen_sa = {}
dict_gen_da = {}


def da_sa_reader(directory_str, real):
    dir_reader = os.fsencode(directory_str)
    for file in os.listdir(dir_reader):
        filename = os.fsdecode(file)
        if filename.endswith(".csv"):
            col_list = ["sa", "da"]
            filename_full = directory_str + "/" + filename
            df = pd.read_csv(filename_full, usecols=col_list)
            csv_sa = df["sa"].tolist()
            csv_da = df["da"].tolist()
            count_sa = {x: csv_sa.count(x) for x in csv_sa}
            count_da = {x: csv_da.count(x) for x in csv_da}
            if real:
                for key in count_sa:
                    if key in dict_real_sa:
                        dict_real_sa[key] = dict_real_sa[key]+count_sa[key]
                    else:
                        dict_real_sa[key] = count_sa[key]
                for key in count_da:
                    if key in dict_real_da:
                        dict_real_da[key] = dict_real_da[key]+count_da[key]
                    else:
                        dict_real_da[key] = count_da[key]
            else:
                for key in count_sa:
                    if key in dict_gen_sa:
                        dict_gen_sa[key] = dict_gen_sa[key]+count_sa[key]
                    else:
                        dict_gen_sa[key] = count_sa[key]
                for key in count_da:
                    if key in dict_gen_da:
                        dict_gen_da[key] = dict_gen_da[key]+count_da[key]
                    else:
                        dict_gen_da[key] = count_da[key]
            continue
        else:
            continue


def da_sa_writer(filename, dataname):
    file = open(filename, "w", newline='')
    writer = csv.writer(file)
    for key, value in dataname.items():
        writer.writerow([key, value])
    file.close()

directory_in_str = "D:/Research/cyberDataGenSite-master/NetVisData/NetVisData"
dir_real1 = directory_in_str + "/real_day1"
dir_real2 = directory_in_str + "/real_day2"
da_sa_reader(dir_real1, True)
da_sa_reader(dir_real2, True)
dir_gen = directory_in_str + "/arcnn_f90"
da_sa_reader(dir_gen, False)

da_sa_writer("D:/Research/cyberDataGenSite-master/NetVisData/real_sa.csv",
             dict_real_sa)
da_sa_writer("D:/Research/cyberDataGenSite-master/NetVisData/real_da.csv",
             dict_real_da)
da_sa_writer("D:/Research/cyberDataGenSite-master/NetVisData/gen_sa.csv",
             dict_gen_sa)
da_sa_writer("D:/Research/cyberDataGenSite-master/NetVisData/gen_da.csv",
             dict_gen_da)
