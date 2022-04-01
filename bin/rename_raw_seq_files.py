"""
rename the seq files according to the datasheeet we were given.
"""
import pandas as pd
import os
class RenameRawSeqFiles:
    def __init__(self):
        """Rename the seq files so that they are in the form given in the associated meta datasheeet"""
        meta_df = pd.read_csv("/home/humebc/projects/20220329_moya/spis_csm/moya_meta_info.csv")
        meta_df.index = meta_df["fastq seq file name"]
        meta_df.set_index("fastq seq file name")
        meta_df.index.name = "sample_name"
        raw_seq_base_dir = "/home/humebc/projects/20220329_moya/spis_csm/raw_seq_data"
        foo = "bar"

        files_to_rename = [_ for _ in os.listdir(raw_seq_base_dir) if _.endswith("fq.gz")]
        for file in files_to_rename:
            sample_name = file.split("_")[0]
            extension = file.split("_")[1]
            new_name = meta_df.at[sample_name, "RNAseq"] + "_" + extension
            old_full = os.path.join(raw_seq_base_dir, file)
            new_full = os.path.join(raw_seq_base_dir, new_name)
            print(f"renaming: {old_full} --> {new_full}")
            os.rename(old_full, new_full)
            

RenameRawSeqFiles()