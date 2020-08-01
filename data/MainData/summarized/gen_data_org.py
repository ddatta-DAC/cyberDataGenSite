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


dict_gen_pr_tcp = {}
dict_gen_pr_udp = {}
dict_gen_pr_icmp = {}


def pr_reader(directory_str):
    dir_reader = os.fsencode(directory_str)
    for file in os.listdir(dir_reader):
        filename = os.fsdecode(file)
        if filename.endswith(".csv"):
            filename_short = filename[8:-6]
            col_list = ["pr"]
            filename_full = directory_str + "/" + filename
            df = pd.read_csv(filename_full, usecols=col_list)
            csv_pr = df["pr"].tolist()
            count_pr = {x: csv_pr.count(x) for x in csv_pr}
            for key in count_pr:
                if key == "TCP":
                    dict_gen_pr_tcp[filename_short] = count_pr[key]
                if key == "UDP":
                    dict_gen_pr_udp[filename_short] = count_pr[key]
                if key == "ICMP":
                    dict_gen_pr_icmp[filename_short] = count_pr[key]
            continue


def pr_writer(filename, dataname):
    file = open(filename, "w", newline='')
    writer = csv.writer(file)
    for key, value in dataname.items():
        writer.writerow([key, value])
    file.close()


directory_in_str = "D:/Research/cyberDataGenSite/NetVisData/NetVisData"

dir_gen = directory_in_str + "/arcnn_f90"
pr_reader(dir_gen)

pr_writer("D:/Research/cyberDataGenSite/NetVisData/gen_pr_tcp.csv",
             dict_gen_pr_tcp)
pr_writer("D:/Research/cyberDataGenSite/NetVisData/gen_pr_udp.csv",
             dict_gen_pr_udp)
pr_writer("D:/Research/cyberDataGenSite/NetVisData/gen_pr_icmp.csv",
             dict_gen_pr_icmp)
