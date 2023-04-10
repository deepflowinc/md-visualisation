#!/bin/bash

python3 pipeline.py \
--input_dir data \
--vtk_saved_dir . \
--input_column_names x y z nx ny nz \
--scale 1 \
--ratio 1 
