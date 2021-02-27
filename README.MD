# COVID-19 Situation Change Script

The script reads COVID-19 statistics from [ECDC](https://www.ecdc.europa.eu/en/geographical-distribution-2019-ncov-cases) and shows changes in 14-day rate of infection cases and deaths per 100K population. The highest infection rate countries are on the top.

### Requirements

The script requires **Python 3.9** and extra module `requests`. The following command can be used to install the module:

```
pip3 install requests
```

### Parameters

By default changes for the latest available week is shown. Different time period can be set by `--from` and `--to` command line options. Values for both options are a year and a week of the year like `2020-32` for 32th week of year 2020. If `--to` option is not set, the latest available week is used. If `--from` option is not set, the previous week for `--to` option is used.

List of countries is taken from `countries` section of `covid.conf` file in the current folder. [ISO 3166-1 alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) country codes are used as keys. If just country code is provided, then the corresponding country name in English is taken from ECDC data. If a value is also provided for a country code, then the value is used as the country name.

Alternative configuration file can be provided with `-c` command line option. If there is no default configuration file or if configuration file is disabled by `-c -` options, then full list of countries is shown.

CSV data file from ECDC can be saved with help of `-s` command line option. Later this file can be used with `-f` option instead of downloading data from ECDC.

### Color Legend

The following table shows meaning of different color for 14-day rate of infection cases and deaths per 100K population:

|    |    cases    |     deaths    |
| -- | :---------: | :-----------: |
| 🟢 |        ≤60  |         ≤1.0  |
| 🟡 |  60< … ≤120 |  1.0< … ≤2.0  |
| 🟠 | 120< … ≤240 |  2.0< … ≤4.0  |
| 🔴 | 240< … ≤480 |  4.0< … ≤8.0  |
| 🟣 | 480< … ≤960 |  8.0< … ≤16.0 |
| 🔵 | 960<        | 16.0<         |

### Examples

Example configuration file:

```ini
[countries]
AUS
CAN
GBR = Great Britain
NZL
USA = Great America
```

The simplest usage of the script showing change between the last two weeks:

```bash
./covid.py
```

And the example output using the example configuration above:

```
from week 2021-06 to week 2021-07
415➚531🟣 13.0➚14.4🟣 Great America
325➘229🟠 16.2➘11.4🟣 Great Britain
115➘110🟡 3.1➘2.4🟠 Canada
1➙1🟢 0.0➙0.0🟢 New Zealand
0➙0🟢 0.0➙0.0🟢 Australia
```

Example of the script usage to show difference betweeb week 52 of year 2020 and the first week of year 2021:

```
./covid.py --from 2020-52 --to 2021-01
```

And the resulting output:

```
from week 2020-52 to week 2021-01
706➚1’091🔵 10.2➚15.2🟣 Great Britain
875➚988🔵 10.3➚12.4🟣 Great America
242➚308🔴 4.1➚5.6🔴 Canada
1➚2🟢 0.0➙0.0🟢 New Zealand
1➙1🟢 0.0➙0.0🟢 Australia
```

To save the current COVID-19 situation statistics from ECDC to file `covid.csv`:

```
./covid.py -s covid.csv
```

And to use the saved data file `covid.csv` to show all countries:

```
./covid.py -f covid.csv -c -
```

Command line option `-c -` disables usage of configuration file.

Here is the top lines of the resulting output:

```
from week 2021-06 to week 2021-07
968➚1’120🔵 17.4➚18.7🔵 Czechia
1168➘1’088🔵 13.7➚18.0🔵 Montenegro
848➚972🔵 14.5➘8.7🟣 San Marino
699➚903🟣 3.1➙3.1🟠 Seychelles
956➘863🟣 10.3➚12.9🟣 Turks and Caicos Islands
```
