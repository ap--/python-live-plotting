#!/bin/bash

for plot in plot*.py; do
    python $plot &
done
