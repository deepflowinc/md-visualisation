import pandas as pd


from utils.tensor import tensor


def df2vtk(df: pd.DataFrame) -> str:
    # input
    # dataframe containing tensor components, file
    # output
    # vtk file which can be used in paraview

    visibs = df['visibility']
    # Picks rows with visibility True, and drops visibility row
    df = df[visibs].drop('visibility', axis=1)

    # Write a buffer that is to be written into .vtk file
    buffer = ['# vtk DataFile Version 5.1\n',
              'vtk output\n', 'ASCII\n', 'DATASET POLYDATA\n']
    buffer.append('POINTS %u float\n' % (df.shape[0]))

    # extract particle locations
    for _, row in df.iterrows():
        buffer.append('%6f %6f %6f\n' % (row['x'], row['y'], row['z']))

    # calculate tensor components to control the shape of the particle
    buffer.append('POINT_DATA %u\n' % (df.shape[0]))
    buffer.append('TENSORS tensors float\n')
    for _, row in df.iterrows():
        XX, YX, ZX, XY, YY, ZY, XZ, YZ, ZZ = tensor(
            row['nx'], row['ny'], row['nz'], row['scale'], row['ratio'])
        buffer.append('%6f %6f %6f %6f %6f %6f %6f %6f %6f\n' %
                      (XX, YX, ZX, XY, YY, ZY, XZ, YZ, ZZ))

    # add scalar information - this helps coloring particles
    for header_column in df.columns.values:
        buffer.append('SCALARS %s float 1\n' % (header_column))
        buffer.append('LOOKUP_TABLE default\n')

        for _, row in df.iterrows():
            buffer.append('%f\n' % (row[header_column]))

    # join strings in buffer
    return ''.join(buffer)
