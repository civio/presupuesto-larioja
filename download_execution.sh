#!/bin/zsh

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <year>"
  exit 1
fi

year=$1

# Create the directory if it doesn't exist
mkdir -p "data/es/comunidad/$year"

# Download the data
curl -o "/tmp/gastos.csv" "https://ias1.larioja.org/opendata/download?r=Y2Q9MTc0fGNmPTAz"
curl -o "/tmp/ingresos.csv" "https://ias1.larioja.org/opendata/download?r=Y2Q9MTc1fGNmPTAz"

# Keep the relevant year only
csvgrep -d ';' -c 1 -m "$year" -e latin_1 "/tmp/gastos.csv" | csvformat -D ';' | tee "data/es/comunidad/$year/ejecucion_gastos.csv" > "data/es/comunidad/$year/gastos.csv"
csvgrep -d ';' -c 1 -m "$year" -e latin_1 "/tmp/ingresos.csv" | csvformat -D ';' | tee "data/es/comunidad/$year/ejecucion_ingresos.csv" > "data/es/comunidad/$year/ingresos.csv" 

