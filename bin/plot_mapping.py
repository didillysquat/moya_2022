"""
Plot up the mapped reads into three categories, zooxs host and other
"""

import os
import gzip
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re

class PlotMapping:
    def __init__(self):
        fastp_dir = "/home/humebc/projects/20220329_moya/spis_csm/fastp"

        host = []
        zooxs = []
        other = []
        samples = list(set([_.split(".")[0] for _ in os.listdir(fastp_dir)]))
        df = pd.DataFrame(0, columns=["host", "zooxs", "unmapped"], index=samples)
        for sample in samples:
            if sample == "T1S1_11wkLT27_-_36_RNASeq_a135":
                foo = "bar"
            # Count each of the zooxs, host and unmapped reads
            host_file = os.path.join(fastp_dir, f"{sample}.host.html")
            if os.path.exists(host_file):
                val = self._search_for_val(host_file)
                df.at[sample, "host"] = val
            
            zooxs_file = os.path.join(fastp_dir, f"{sample}.zooxs.html")
            if os.path.exists(zooxs_file):
                val = self._search_for_val(zooxs_file)
                df.at[sample, "zooxs"] = val

            unmapped_file = os.path.join(fastp_dir, f"{sample}.unmapped.html")
            if os.path.exists(unmapped_file):
                val = self._search_for_val(unmapped_file)
                df.at[sample, "unmapped"] = val

        # Now plot up the results
        fig, ax = plt.subplots(figsize=(15, 15))

        ax.bar(samples, df["host"], 1, label='host', color="#0400ff")
        ax.bar(samples, df["zooxs"], 1, label='zooxs', bottom=df["host"], color="#00ff00")
        ax.bar(samples, df["unmapped"], 1, label='other', bottom=df["host"] + df["zooxs"], color="#ff0200")

        ax.set_ylabel('reads')
        ax.set_title('Number of reads by origin')
        ax.legend()
        plt.xticks(rotation = 90)
        plt.tight_layout()
        plt.savefig("/home/humebc/projects/20220329_moya/spis_csm/figures/mapped_read_count_stacked_bar.png", dpi=600)

        # Now stacked with zooxs only
        fig, ax = plt.subplots(figsize=(15, 15))
        ax.bar(samples, df["zooxs"], 1, label='zooxs', color="#00ff00")
        ax.set_ylabel('reads')
        ax.set_title('Number of reads by origin')
        ax.legend()
        plt.xticks(rotation = 90)
        plt.tight_layout()
        plt.savefig("/home/humebc/projects/20220329_moya/spis_csm/figures/mapped_read_count_stacked_bar_zooxs_only.png", dpi=600)

        df.to_csv("/home/humebc/projects/20220329_moya/spis_csm/mapped_reads_table/reads_mapped.tsv", sep="\t", index=True)

        # Now do a 3 subplots with each with host, zooxs or other as mean with sd bars
        fig, ax = plt.subplots(figsize=(15, 15))
        ax.boxplot(df, labels=list(df))
        plt.savefig("/home/humebc/projects/20220329_moya/spis_csm/figures/box.png", dpi=600)

        # Now do one that is just zooxs
        fig, ax = plt.subplots(figsize=(15, 15))
        ax.boxplot(df["zooxs"], labels=["zooxs"])
        ax.set_yticks(np.arange(0, 12000000, 250000))
        ax.grid(visible=True)
        plt.savefig("/home/humebc/projects/20220329_moya/spis_csm/figures/box_only_zooxs.png", dpi=600)

        foo = "bar"

    def _search_for_val(self, host_file):
        print(f"reading in {host_file}")
        with open(host_file, "r") as f:
            for line in [_.rstrip() for _ in f]:
                if "reads passed filters:" in line:
                    str_val = re.search("\d+\.\d+ [M,K]", line)[0]
                    comp = str_val.split(" ")
                    if comp[-1] == "M":
                        return int(float(comp[0]) * 1000000) 
                    elif comp[-1] == "K":
                        return int(float(comp[0]) * 1000)
                    else:
                        raise RuntimeError

                    foo = "bar"
PlotMapping()