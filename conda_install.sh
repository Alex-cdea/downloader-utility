#!/bin/bash

PREFIX=$(realpath $1)

if [ -z "$PREFIX" ]
then
  echo "Error: you must provide a path."
  exit
fi

sed -i "s+PREFIX+${PREFIX}+" \
downloader-utility.yml


if [ -z "$(command -v conda)" ]
then
  echo "Error: conda is not installed."
  exit
fi

eval "$(conda shell.bash hook)"

conda env create -p $PREFIX/downloader-utility_1/ -f downloader-utility.yml

if [ $? -eq 0 ]
then
  mkdir -p $PREFIX/downloader-utility_1/share/
  cd ../
  mv downloader-utility/ $PREFIX/downloader-utility_1/share/
  chmod +x $PREFIX/downloader-utility_1/share/downloader-utility/app/downloader-utility.py
  ln -s $PREFIX/downloader-utility_1/share/downloader-utility/app/downloader-utility.py \
  $PREFIX/downloader-utility_1/downloader-utility.py
  sed -i "s+file_tax =.*+file_tax = \"$PREFIX/downloader-utility_1/share/downloader-utility/taxonomy/Eukaryota_tax.tsv.tar.gz\"+" \
  $PREFIX/downloader-utility_1/share/downloader-utility/app/downloader-utility.py
  echo "downloader-utility has been successfully installed."
else
  source env create -f downloader-utility.yml
  if [ $? -eq 0 ]
  then
      mkdir -p $PREFIX/downloader-utility_1/share/
      cd ../
      mv downloader-utility/ $PREFIX/downloader-utility_1/share/
      chmod +x $PREFIX/downloader-utility_1/share/downloader-utility/app/downloader-utility.py
      ln -s $PREFIX/downloader-utility_1/share/downloader-utility/app/downloader-utility.py \
      $PREFIX/downloader-utility_1/downloader-utility.py
      sed -i "s+file_tax =.*+file_tax = \"$PREFIX/downloader-utility_1/share/downloader-utility/taxonomy/Eukaryota_tax.tsv.tar.gz\"+" \
      $PREFIX/downloader-utility_1/share/downloader-utility/app/downloader-utility.py
      echo "downloader-utility has been successfully installed."
  else
    echo "Error: a problem occurred. Could not install downloader-utility."
    exit
  fi
fi
