#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 19:00:12 2019

The aim of this script is to find view for a selected gene and for a selected
TCGA cohort (optional)
Here we assume that we have harmonized MAF file from a mutation caller
and we also have a csv file generated from dalmatian_helper.py

@author: qingzhang
"""

def find_view(cs, dal, gene, cohort=None):
    gene = gene.upper()
    cs = cs.dropna()
    dal = dal.dropna()
    cs = cs[cs["gene"].str.match(gene)]
    print("There are ", cs.shape[0], "matching the query gene:", gene)
    if cohort: # an optional filter for , eg BRCA
        cohort = cohort.upper()
        cs = cs[cs["ttype"].str.match(cohort)]
        dal = dal[dal["cohort"].str.match(cohort)]
        print("There are ",cs.shape[0], "matching query cohort:", cohort)
    # get the 6 digit identifier from pids in MC3
    pid6 = [pid[5:12] for pid in cs["patient"].tolist()]
    # the aim pid6 from dal is
    dal["pid6"] = dal["tss"].str.cat(dal["pid"], sep = "-")
    # filter MC3 callset by if contains the desired pid6
    ans = dal[dal["pid6"].isin(pid6)].reset_index()
    if ans.shape[0] == 0:
        print("no sample matched with query")
    else:
        resl = []
        for i in range(ans.shape[0]):
            print(i)
            resdict = {
                    "cohort" : ans["cohort"][i],
                    "pid6" : ans["pid6"][i],
                    "gene" : gene,
                    "posdf" : cs[cs["patient"].str.contains(ans["pid6"][i])][["chr","pos"]]
            }
            resl.append(resdict)
    return resl



if __name__ == "__main__":
    import pandas as pd
    cs = pd.read_csv("../testdata/test_callset.txt", delimiter="\t")
    # read in the dataframe generated by dalmatian helper
    dal = pd.read_csv("../testdata/matched_paires_with_tss.csv", index_col = [0])
    dal["pid6"] = dal["tss"].str.cat(dal["pid"], sep = "-")
    a = find_view(cs, dal, "KRAS", "LIHC")
