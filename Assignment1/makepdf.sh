file=$1
pandoc -s $file.markdown -o $file.tex -V geometry:margin=0.8in
pdflatex $file.tex
rm *.aux *.log *~ *.out -rf

