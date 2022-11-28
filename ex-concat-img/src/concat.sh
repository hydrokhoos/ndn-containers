cat *.csv | head -n 1 > tmp && find -name "*.csv" -exec sed -e '1d' {} \; >> tmp;
mv tmp result.csv
