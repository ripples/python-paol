#!/bin/bash

# Set the first argument as the lecture directory to upload
outDir=$1

cd $outDir
cd whiteboard
for image in *.png
do
    if [[ $image = *"-thumb"* ]]; then
        continue
    else
        convert $image -resize 100x100 ${image%.*}-thumb.png
    fi
done

cd ../blackboard
for image in *.png
do
    if [[ $image = *"-thumb"* ]]; then
        continue
    else
        convert $image -resize 100x100 ${image%.*}-thumb.png
    fi
done

cd ../computer
for image in *.png
do
    if [[ $image = *"-thumb"* ]]; then
        continue
    else
        convert $image -resize 100x100 ${image%.*}-thumb.png
    fi
done
