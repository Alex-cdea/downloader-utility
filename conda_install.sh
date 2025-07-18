#!/bin/bash

PREFIX=$1

sed -i "s+PREFIX+${PREFIX}+" \
downloader-utility.yml


if [ -z "$(command -v conda)" ]
then
  echo "Error: conda is not installed."
  exit
fi

eval "$(conda shell.bash hook)"

conda env create -f downloader-utility.yml

if [ $? -eq 0 ]
then
  echo "downloader-utility has been successfully installed."
else
  source env create -f downloader-utility.yml
  if [ $? -ne 0 ]
  then
    echo "Error: a problem occurred. Could not install downloader-utility."
    exit
  fi
fi
