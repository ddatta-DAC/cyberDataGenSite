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

byt_tcp = []
byt_udp = []
byt_icmp = []

def byt_reader(directory_str):
    dir_reader = os.fsencode(directory_str)
    for file in os.listdir(dir_reader):
        filename = os.fsdecode(file)
        if filename.endswith(".csv"):
            filename_short = filename[8:-6]
            col_list = ["byt","pr"]
            filename_full = directory_str + "/" + filename
            df = pd.read_csv(filename_full, usecols=col_list)
            csv_byt_tcp = df[df["pr"]=="TCP"]["byt"]
            byt_tcp.extend(csv_byt_tcp)
            csv_byt_udp = df[df["pr"]=="UDP"]["byt"]
            byt_udp.extend(csv_byt_udp)
            csv_byt_icmp = df[df["pr"]=="ICMP"]["byt"]
            byt_icmp.extend(csv_byt_icmp)
            continue


def byt_writer(filename, dataname):
    
    with open(filename, 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(dataname)
    


directory_in_str = "D:/Research/cyberDataGenSite/NetVisData/NetVisData"

dir_gen = directory_in_str + "/arcnn_f90"
byt_reader(dir_gen)

byt_writer("D:/Research/cyberDataGenSite/NetVisData/gen_byt_tcp.csv", byt_tcp)
byt_writer("D:/Research/cyberDataGenSite/NetVisData/gen_byt_udp.csv", byt_udp)
byt_writer("D:/Research/cyberDataGenSite/NetVisData/gen_byt_icmp.csv", byt_icmp)
