# COVID-19 Situation Change Script

The script reads COVID-19 statistics from [ECDC](https://www.ecdc.europa.eu/en/geographical-distribution-2019-ncov-cases) and shows changes in 14-day rate of infection cases and deaths per 100K population. The highest infection rate countries are on the top.

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
