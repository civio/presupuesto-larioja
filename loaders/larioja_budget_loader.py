# -*- coding: UTF-8 -*-
from budget_app.models import *
from budget_app.loaders import SimpleBudgetLoader
import re

class LaRiojaBudgetLoader(SimpleBudgetLoader):

    def parse_item(self, filename, line):
        return None