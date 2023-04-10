# libraries
from pathlib import Path
from typing import Optional, Tuple
import argparse
import pandas as pd
import os
import json

from utils.add_visualise_params import add_visualise_params
from utils.df2vtk import df2vtk


# input arguments
# Create the parser
def parse_agrs():
    parser = argparse.ArgumentParser(
        description='program to which takes the result from MD, then visualise it using Paraview')
    parser.add_argument(
        '--input_dir', help='Provide a path to a directory containing input files', required=True)
    parser.add_argument('--vtk_saved_dir', default='.',
                        help='Provide a directory path to save processed vtk file', type=Path)
    parser.add_argument('--save_csv', action='store_true',
                        help='if spcified, the program saves the processed csv file')
    parser.add_argument(
        '--save_video', help='if specified, the program creates .vtk.series file which can be animated in Paraview', action='store_true')
    parser.add_argument('--input_column_names', nargs='+', default=[
                        'x', 'y', 'z', 'nx', 'ny', 'nz'], help='header of the data file you are processing', type=str)
    parser.add_argument('--input_skip_first_line',
                        help='if specified, skips the first line of the input',
                        action='store_true')
    parser.add_argument(
        '--scale', default=1, help='Scale determines the radius of particles. Every particles will have the same scale', type=float)
    parser.add_argument('--ratio', default=1, help='Ratio determines the shape of particles. The parameter is the ratio of the long and short axis(long/short), which are the length of the eigenvectors. Every particles will have the same ratio', type=float)
    parser.add_argument(
        "--threshold", nargs=3, help='For a given scalar, extract particles inside the lower bound and upper bound for visualisation. e.g. scale 0 5 means extracting particles which scale is >= 0 and <= 5', type=str)
    parser.add_argument("--cross_section_grad", nargs=4,
                        help='parameter to define the gradient of the plane', type=float)
    parser.add_argument(
        "--cross_section_width", help='width of 2 plane cutting the 3D particle models', type=float)
    parser.add_argument("--cross_section_origin", nargs=3,
                        default=[0, 0, 0], help='origin of the plane', type=float)
    args = parser.parse_args()
    return args


# single data to vtk
def vtk_generator(file: Path, column_names: str, skip_first_line: bool, vtk_saved_dir: Path, save_csv: bool,
                  scale: float, ratio: float,
                  plane_grad: Optional[Tuple[float, float, float, float]],
                  plane_width: Optional[float],
                  plane_origin: Tuple[float, float, float],
                  threshold: Optional[Tuple[str, float, float]]
                  ):

    print(f'Processing {file}')

    # load .dat file, convert .dat to dataframe
    filename, file_extension = os.path.splitext(file)
    separator = ","
    if file_extension == ".dat":
        separator = " "

    if skip_first_line:
        df = pd.read_csv(file, sep=separator, names=column_names, header=0)
    else:
        df = pd.read_csv(file, sep=separator, names=column_names)

    # add more information into dataframe. e.g. angles, color etc
    add_visualise_params(df, scale, ratio, plane_grad,
                         plane_width, plane_origin, threshold)
    if save_csv:
        # save csv file
        csv = os.path.join(vtk_saved_dir,
                           os.path.basename(filename)) + ".csv"
        df.to_csv(csv, index=False, header=column_names)
        print(f'saved csv {os.path.basename(csv)} to {vtk_saved_dir}')

    # create vtk from dataframe
    vtk_string = df2vtk(df)
    # extract the filename of input.dat
    base = os.path.basename(file)
    filename = os.path.splitext(base)[0]
    # output file has the same name as the inout file but is .vtk
    filepath = os.path.join(vtk_saved_dir, filename + '.vtk')

    # write it into a file
    with open(filepath, 'w') as f:
        f.write(vtk_string)

    print(f'Processed {file}\n')


# function to create .vtk.series from multiple
def vtkseries_gen(vtk_saved_dir: Path):
    # takes vtk files in a list
    files = [os.path.join(vtk_saved_dir, file)
             for file in os.listdir(vtk_saved_dir) if file.endswith('.vtk')]
    # sort the list
    files.sort()
    print('combining following files to create .vtk.series file')
    print(files)

    # take filename from one of the files and remove number
    filename = os.path.basename(files[0])  # takes base filename
    filename = os.path.splitext(filename)[0]  # remove extension
    filename = ''.join(
        (x for x in filename if not x.isdigit()))  # remove digits
    filepath = os.path.join(vtk_saved_dir, filename + '.vtk.series')

    # iterate through vtk files in the directory
    vtk_series = []
    for time, file in enumerate(files):
        item = {"name": os.path.basename(file), "time": time}
        vtk_series.append(item)

    # save into .vtk.series as a json format
    string = {
        "file-series-version": "1.0",
        "files": vtk_series
    }

    jsonString = json.dumps(string, indent=2)
    with open(filepath, "w") as jsonFile:
        jsonFile.write(jsonString)


def pipeline():
    # takes input data directory path
    args = parse_agrs()

    # validate user inputs
    # check whether the given directories exist
    if not os.path.exists(args.input_dir):
        raise Exception(f"The input directory '{args.input_dir}' does not exist.") 

    if not os.path.exists(args.vtk_saved_dir):
        print(f"The directory to save vtk files '{args.vtk_saved_dir}' does not exist. The program will create the directory") 
        os.mkdir(args.vtk_saved_dir)

    # check threshold of max >= min
    if args.threshold:
        scalar_lb = float(args.threshold[1])
        scalar_ub = float(args.threshold[2])
        if scalar_lb > scalar_ub:
            raise Exception(f"The value of the lower bound ({scalar_lb}) is greater than the upper bound ({scalar_ub}). Please change the order and run the code again.)") 

    files = [os.path.join(args.input_dir, file)
             for file in os.listdir(args.input_dir)]

    # run pipeline for each file
    for file in files:
        vtk_generator(file, args.input_column_names, args.input_skip_first_line,
                      args.vtk_saved_dir, args.save_csv, args.scale, args.ratio, args.cross_section_grad,
                      args.cross_section_width, args.cross_section_origin, args.threshold)

    if args.save_video:
        vtkseries_gen(args.vtk_saved_dir)
        print('saved .vtk.series file')

    print('Completed pipeline')


if __name__ == '__main__':
    pipeline()
