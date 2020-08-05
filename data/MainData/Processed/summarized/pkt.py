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

pkt_tcp = []
pkt_udp = []
pkt_icmp = []

def pkt_reader(directory_str):
    dir_reader = os.fsencode(directory_str)
    for file in os.listdir(dir_reader):
        filename = os.fsdecode(file)
        if filename.endswith(".csv"):
            filename_short = filename[8:-6]
            col_list = ["pkt","pr"]
            filename_full = directory_str + "/" + filename
            df = pd.read_csv(filename_full, usecols=col_list)
            csv_pkt_tcp = df[df["pr"]=="TCP"]["pkt"]
            pkt_tcp.extend(csv_pkt_tcp)
            csv_pkt_udp = df[df["pr"]=="UDP"]["pkt"]
            pkt_udp.extend(csv_pkt_udp)
            csv_pkt_icmp = df[df["pr"]=="ICMP"]["pkt"]
            pkt_icmp.extend(csv_pkt_icmp)
            continue


def pkt_writer(filename, dataname):
    
    with open(filename, 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(dataname)
    


directory_in_str = "D:/Research/cyberDataGenSite/NetVisData/NetVisData"

dir_gen = directory_in_str + "/arcnn_f90"
pkt_reader(dir_gen)

pkt_writer("D:/Research/cyberDataGenSite/NetVisData/gen_pkt_tcp.csv", pkt_tcp)
pkt_writer("D:/Research/cyberDataGenSite/NetVisData/gen_pkt_udp.csv", pkt_udp)
pkt_writer("D:/Research/cyberDataGenSite/NetVisData/gen_pkt_icmp.csv", pkt_icmp)
