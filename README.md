# Plot COVID-19 case numbers

This script plots COVID-19 case numbers. By default, the total numbers
(globally) are plotted. Numbers for individual countries can be plotted
via the `-c`/`--countries` option. The data can be updated with the
`-d`/`--download` option.

Running the script in an `IPython` session:

``` ipython
run plot_covid-19.py -e png -c Australia -s -d
run plot_covid-19.py -e png -c Australia Germany Finland -d
```

The data is obtained from the
[CSSEGISandData/COVID-19](https://github.com/CSSEGISandData/COVID-19) repository
on GitHub, maintained by the
[Johns Hopkins University Center for Systems Science and Engineering (JHU CSSE)](https://systems.jhu.edu/).
