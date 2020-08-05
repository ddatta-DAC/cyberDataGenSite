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

td_tcp = []
td_udp = []
td_icmp = []

def td_reader(directory_str):
    dir_reader = os.fsencode(directory_str)
    for file in os.listdir(dir_reader):
        filename = os.fsdecode(file)
        if filename.endswith(".csv"):
            filename_short = filename[8:-6]
            col_list = ["td","pr"]
            filename_full = directory_str + "/" + filename
            df = pd.read_csv(filename_full, usecols=col_list)
            csv_td_tcp = df[df["pr"]=="TCP"]["td"]
            td_tcp.extend(csv_td_tcp)
            csv_td_udp = df[df["pr"]=="UDP"]["td"]
            td_udp.extend(csv_td_udp)
            csv_td_icmp = df[df["pr"]=="ICMP"]["td"]
            td_icmp.extend(csv_td_icmp)
            continue


def td_writer(filename, dataname):
    
    with open(filename, 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(dataname)
    


directory_in_str = "D:/Research/cyberDataGenSite/NetVisData/NetVisData"

dir_gen = directory_in_str + "/arcnn_f90"
td_reader(dir_gen)

td_writer("D:/Research/cyberDataGenSite/NetVisData/gen_td_tcp.csv", td_tcp)
td_writer("D:/Research/cyberDataGenSite/NetVisData/gen_td_udp.csv", td_udp)
td_writer("D:/Research/cyberDataGenSite/NetVisData/gen_td_icmp.csv", td_icmp)
