#!/bin/bash

mkdir -p ./out

num_lect="05"

if [ -n "$1" ]; then
  # Если передан номер примера, компилируем соответствующий файл
  example_file="src/${num_lect}_${1}.cpp"
  
  if [ -f "$example_file" ]; then
    g++ -std=c++20  -c "${example_file}" -o "out/${num_lect}_${1}.o"
    g++ "out/${num_lect}_${1}.o" -o "${num_lect}_${1}.exe"
  else
    echo "Пример с номером $1 не найден"
  fi
else
  # Если номер не передан, компилируем все примеры по отдельности
  for example_file in "src/${num_lect}_"*.cpp; do
    if [ -f "$example_file" ]; then
      filename=$(basename -- "$example_file")
      filename="${filename%.*}"
      g++ -std=c++20 -c "${example_file}" -o "out/${filename}.o"
      g++ "out/${filename}.o" -o "${filename}.exe"
    fi
  done
fi