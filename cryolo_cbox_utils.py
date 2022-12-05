# Imports
import numpy as np
import pandas as pd
from pandas import DataFrame
from pathlib import Path
import os
from cmath import nan


# Functions

def filter_data_rows(new_cbox_str:str) -> list: 


    filtered_rows:list = []
    for row in new_cbox_str.split("\n"):
        fields = row.split(" ")
        if len(fields) > 2:
            filtered_rows.append(fields)
    return filtered_rows


def get_column_names(new_cbox_str) -> list:


    column_names = []
    rows = new_cbox_str.split("\n")

    for i, row in enumerate(rows):
        if row == "loop_":
            print("Column names detected:")
            j = 1
            fields = []
            while len(fields) < 3:
                row2 = rows[i+j]
                fields = row2.split(" ")
                if not len(fields) < 3:
                    break
                column_name = fields[0].strip("_")
                column_names.append(column_name)
                print(f"{fields} -> {column_name}")
                j += 1
            break

    return column_names

def parse_new_cbox_format(new_cbox_file_path) -> DataFrame:

    with open(new_cbox_file_path, mode="r") as f:
        new_cbox_particles_str = f.read()
    
    filtered_rows = filter_data_rows(new_cbox_particles_str)
    column_names = get_column_names(new_cbox_particles_str)

    particle_df = DataFrame(
        data=filtered_rows,
        columns=column_names,
        dtype=float
    )

    particle_df[particle_df == "<NA>"] = nan

    return particle_df

def write_in_old_cbox_format(particles_df_clean:DataFrame) -> str:


    assert not particles_df_clean.isna().any().any()

    old_cbox_output = ""

    for i, row_series in particles_df_clean.iterrows():
        
        # The assignment is guesswork to a certain degree
        row_str = f"{np.round(row_series.CoordinateX,1)}\t{np.round(row_series.CoordinateY,1)}\t{int(row_series.Width)}\t{int(row_series.Height)}\t{row_series.Confidence}\t{int(row_series.EstWidth)}\t{int(row_series.EstHeight)}"

        old_cbox_output += row_str + "\n"
    
    return old_cbox_output

# Constants:

OLD_FORMAT_SIGNIFIER = "OLD_FORMAT"



###################################################################

def main():

    example_cbox_file = Path("example_CBOX_files_new_format/FoilHole_8535783_Data_6461108_6461110_20220309_161226_fractions.cbox")

    particles_df = parse_new_cbox_format(example_cbox_file)

    print(particles_df)

    particles_df_clean = particles_df.dropna(axis=1, how="all")

    old_cbox_output = write_in_old_cbox_format(particles_df_clean)
    example_old_cbox_output_path = example_cbox_file.parent / Path(f"{example_cbox_file.stem}_{OLD_FORMAT_SIGNIFIER}.cbox")
    with open(example_old_cbox_output_path, mode="w") as f:
        f.write(old_cbox_output)




if __name__ == "__main__":
    main()