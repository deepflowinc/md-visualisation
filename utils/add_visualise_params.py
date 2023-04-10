from typing import Optional, Tuple
import numpy as np
import pandas as pd


def add_visualise_params(
        df: pd.DataFrame, scale: float, ratio: float,
        cross_section_grad: Optional[Tuple[float, float, float, float]],
        cross_section_width: Optional[float],
        cross_section_origin: Tuple[float, float, float],
        threshold: Optional[Tuple[str, float, float]]):
    # this function adds additional information into the dataframe
    # the dataframe is later used in writing .vtk file

    # add column 'scale' and 'ratio'
    if not ('scale' in df.columns):
        print(
            f"There is no column 'scale' in the input data, adding 'scale = {scale}' from the input arguments.")
        df['scale'] = scale

    if not ('ratio' in df.columns):
        print(
            f"There is no column 'ratio' in the input data, adding 'ratio = {ratio}' from the input arguments.")
        df['ratio'] = ratio

    # add column 'nx', 'ny', 'nz' if not specified by users
    if not ('nx' in df.columns and 'ny' in df.columns and 'nz' in df.columns):
        print(f"There is no information about long-axis in the input data. The program will generate a visualisation of spheres")
        df['nx'] = 1
        df['ny'] = 0
        df['nz'] = 0

    if ('theta' in df.columns or 'phi' in df.columns):
        print('theta or phi already exist in df, overwriting them')
    # convert from radian to degrees for more intuitive visualisation
    d = 180/np.pi
    # add column 'theta' from nx and ny
    df['theta'] = np.arctan2(df['ny'], df['nx'])*d
    # add column 'phi' from nz
    df['phi'] = np.arccos(np.absolute(df['nz']))*d

    # define a plane to extract cross section
    if cross_section_grad is not None:
        a = cross_section_grad[0]
        b = cross_section_grad[1]
        c = cross_section_grad[2]
        d = cross_section_grad[3]
        x0 = cross_section_origin[0]
        y0 = cross_section_origin[1]
        z0 = cross_section_origin[2]
        print(
            f"Plane equation of the cross section is specified and is ({a})x + ({b})y + ({c})z + ({d}) = 0")
        print(f"Cross section goes through a point ({x0}, {y0}, {z0})")
        cross_section_flag = True
    else:
        cross_section_flag = False

    # if width of the planes are not provided via ars, it uses the value form args.scale
    w: float = cross_section_width or df.at[0, 'scale']
    print(f"Width of the cross section is {w}")

    # extract particles to visualise
    # do this by adding column 'visibility'
    for i, row in df.iterrows():
        visible: bool = True

        if cross_section_flag:  # run this block if plane is defined
            # ensure the particles' origin satisfie the condition that they are inside 2 planes
            cross_section_ub: bool = (a*(row['x']-x0) + b *
                                 (row['y']-y0) + c*(row['z']-z0) + d - w/2 < 0)
            cross_section_lb: bool = (a*(row['x']-x0) + b *
                                 (row['y']-y0) + c*(row['z']-z0) + d + w/2 > 0)
            visible = cross_section_ub and cross_section_lb

        if threshold is not None:
            scalar_variable: str = threshold[0]
            scalar_lb: float = float(threshold[1])
            scalar_ub:float = float(threshold[2])
            
            visible = visible and (row[scalar_variable] <= scalar_ub) and (row[scalar_variable] >= scalar_lb)

        df.at[i, 'visibility'] = visible

    if threshold is not None:
        print(
            f"Extracted particles which {threshold[0]} is between {threshold[1]} and {threshold[2]}.")

    print(f'header of the processed dataframe: {df.columns.values}')
    print(df.head())
