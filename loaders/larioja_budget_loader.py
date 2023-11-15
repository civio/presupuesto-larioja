# -*- coding: UTF-8 -*-
from budget_app.loaders import SimpleBudgetLoader


expenses_mapping = {
    'default': { 'ic_code': 3, 'fc_code': 19, 'full_ec_code': 11, 'description': 12, 'forecast_amount': 21, 'actual_amount': 26 },
}

income_mapping = {
    'default': { 'full_ec_code': 7, 'description': 8, 'forecast_amount': 9, 'actual_amount': 12 },
}


class BudgetCsvMapper:
    def __init__(self, year, is_expense):
        column_mapping = income_mapping

        if is_expense:
            column_mapping = expenses_mapping

        mapping = column_mapping.get(str(year))

        if not mapping:
            mapping = column_mapping.get('default')

        self.ic_code = mapping.get('ic_code')
        self.fc_code = mapping.get('fc_code')
        self.full_ec_code = mapping.get('full_ec_code')
        self.description = mapping.get('description')
        self.forecast_amount = mapping.get('forecast_amount')
        self.actual_amount = mapping.get('actual_amount')


class LaRiojaBudgetLoader(SimpleBudgetLoader):
    # make year data available in the class and call super
    def load(self, entity, year, path, status):
        self.year = year
        SimpleBudgetLoader.load(self, entity, year, path, status)

    # Parse an input line into fields
    def parse_item(self, filename, line):
        # Skip header
        if line[0]=='EJERCICIO':
            return

        # Type of data
        is_expense = (filename.find('gastos.csv') != -1)
        is_actual = (filename.find('/ejecucion_') != -1)

        # Mapper
        mapper = BudgetCsvMapper(self.year, is_expense)

        # Economic code: we need to remove the hyphens
        full_ec_code = line[mapper.full_ec_code].replace('-', '')
        # Concepts are the first three digits
        # Item numbers are the last two digits (fourth and fifth digits)
        ec_code = full_ec_code[:3]
        item_number = full_ec_code[-2:]

        # Description
        description = line[mapper.description].decode('latin-1')

        # Parse amount
        amount = line[mapper.actual_amount if is_actual else mapper.forecast_amount]
        amount = self._read_spanish_number(amount)

        # Expenses
        if is_expense:
            # Institutional code
            # The code is 4-6 characters long, but we ignore anything after the 4th character.
            ic_code = (line[mapper.ic_code].replace('-', ''))+'0'

            # Functional code
            fc_code = line[mapper.fc_code].replace('-', '')

        # Income
        else:
            # We don't have institutional or functional codes in income
            fc_code = None
            ic_code = '00000'

        return {
            'is_expense': is_expense,
            'is_actual': is_actual,
            'fc_code': fc_code,
            'ec_code': ec_code,
            'ic_code': ic_code,
            'ic_institution': ic_code[0:2],
            'ic_section': ic_code[0:4],
            'ic_department': ic_code,
            'item_number': item_number,
            'description': description,
            'amount': amount
        }

    def _get_delimiter(self):
        return ';'
