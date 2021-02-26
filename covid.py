#!/usr/bin/env python3

import requests

from argparse import ArgumentParser
from configparser import ConfigParser
from csv import DictReader
from itertools import groupby
from operator import attrgetter, itemgetter

COVID_LINK = 'https://opendata.ecdc.europa.eu/covid19/nationalcasedeath/csv'

COUNTRIES_SECTION = 'countries'
COUNTRY_CODE = 'country_code'
COUNTRY = 'country'
INDICATOR = 'indicator'
WEEK = 'year_week'
CASES = 'cases'
DEATHS = 'deaths'
RATE = 'rate_14_day'


class CovidCountry:
    def __init__(self, country, data):
        self.name = country
        indicators = self._groupped(data, itemgetter(INDICATOR))
        (self.case_rate_from, self.case_rate_to) = self._rates(indicators[CASES])
        (self.death_rate_from, self.death_rate_to) = self._rates(indicators[DEATHS])

    def __repr__(self):
        class_name = self.__class__.__name__
        attrs = ', '.join('{}: {!r}'.format(key, value) for key, value in self.__dict__.items())
        return f'{class_name}({attrs})'

    @staticmethod
    def _groupped(data, discriminator):
        return dict([(key, list(value)) for key, value in groupby(data, discriminator)])

    @staticmethod
    def _rates(data):
        weeks = CovidCountry._groupped(data, itemgetter(WEEK))
        data_from = weeks[min(weeks.keys())][0]
        data_to = weeks[max(weeks.keys())][0]
        return (float(data_from[RATE] or 0), float(data_to[RATE] or 0))


def covid_data(data_file, save_file):
    if data_file:
        with open(data_file, encoding='utf-8-sig') as covid_file:
            return list(DictReader(covid_file))
    else:
        response = requests.get(COVID_LINK)
        if response:
            text = response.text
            if save_file:
                with open(save_file, 'w', encoding='utf-8-sig') as copy:
                    copy.write(text)
            return list(DictReader(text.splitlines()))
        else:
            response.raise_for_status()


def selected_countries(config_file, data):
    config = ConfigParser(allow_no_value=True)
    config.optionxform = lambda option: option.upper()
    config.read(config_file, encoding='utf-8')
    countries = dict([(key, list(value)[0][COUNTRY]) for key, value in groupby(data, itemgetter(COUNTRY_CODE))])

    if COUNTRIES_SECTION in config:
        return dict([(key, value if value else countries[key]) for key, value in config.items(COUNTRIES_SECTION) if key in countries])
    else:
        return countries


def countries_and_weeks(selected_countries, week_from, week_to):
    def predicate(data):
        return (data[COUNTRY_CODE] in selected_countries and (data[WEEK] == week_from or data[WEEK] == week_to))
    return predicate


def covid_country(selected_countries):
    def transformer(tuple):
        (country_code, data) = tuple
        return CovidCountry(selected_countries[country_code], list(data))
    return transformer


def round_cases(cases_rate):
    return int(round(cases_rate))


def round_deaths(deaths_rate):
    return round(deaths_rate/10, 1)


def trend(rate_from, rate_to):
    if rate_from > rate_to:
        return '➘'
    if rate_from < rate_to:
        return '➚'
    else:
        return '➙'


def level_cases(rate):
    if rate <= 60:
        return '🟢'
    if rate <= 120:
        return '🟡'
    if rate <= 240:
        return '🟠'
    if rate <= 480:
        return '🔴'
    if rate <= 960:
        return '🟣'
    else:
        return '🔵'


def level_deaths(rate):
    if rate <= 1:
        return '🟢'
    if rate <= 2:
        return '🟡'
    if rate <= 4:
        return '🟠'
    if rate <= 8:
        return '🔴'
    if rate <= 16:
        return '🟣'
    else:
        return '🔵'


def valid_week(week, weeks, default):
    if week in weeks:
        return week
    if not week:
        return default
    else:
        print(f'❌ wrong week provided: {week}')
        return None


def valid_weeks(week_from, week_to, data):
    weeks = set(map(itemgetter(WEEK), data))
    weeks_sorted = sorted(weeks)
    week_min = min(weeks)
    week_max = max(weeks)
    week_to = valid_week(week_to, weeks, week_max)
    week_from = valid_week(week_from, weeks, weeks_sorted[max(weeks_sorted.index(week_to or week_min) - 1, 0)])
    if week_from and week_to:
        return (week_from, week_to)
    else:
        print(f'❕ available weeks: from {week_min} to {week_max}')
        return (None, None)


def change(week_from, week_to, config_file, data_file, save_file):
    data = covid_data(data_file, save_file)
    (week_from, week_to) = valid_weeks(week_from, week_to, data)
    if not week_to:
        return

    country_dict = selected_countries(config_file, data)

    print(f'from week {week_from} to week {week_to}')
    countries = list(map(covid_country(country_dict), groupby(filter(countries_and_weeks(
        country_dict, week_from, week_to), data), itemgetter(COUNTRY_CODE))))
    for country in sorted(countries, key=attrgetter('case_rate_to'), reverse=True):
        case_rate_from = round_cases(country.case_rate_from)
        case_rate_to = round_cases(country.case_rate_to)
        case_trend = trend(case_rate_from, case_rate_to)
        case_level = level_cases(case_rate_to)

        death_rate_from = round_deaths(country.death_rate_from)
        death_rate_to = round_deaths(country.death_rate_to)
        death_trend = trend(death_rate_from, death_rate_to)
        death_level = level_deaths(death_rate_to)

        print((f'{case_rate_from}{case_trend}{case_rate_to:,}{case_level} '
               f'{death_rate_from}{death_trend}{death_rate_to:,}{death_level} '
               f'{country.name}').replace(',', '’'))


parser = ArgumentParser(description='change of COVID-19 situation')
parser.add_argument('--from', metavar='year-week', dest='week_from')
parser.add_argument('--to', metavar='year-week', dest='week_to')
parser.add_argument('-c', '--config', metavar='config-file', dest='config_file', default='covid.conf')
parser.add_argument('-s', '--save', metavar='csv-file', dest='save_file')
parser.add_argument('-f', '--file', metavar='csv-file', dest='data_file')
args = parser.parse_args()

change(args.week_from, args.week_to, args.config_file, args.data_file, args.save_file)
