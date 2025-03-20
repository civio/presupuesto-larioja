import six

if six.PY2:
    from larioja_budget_loader import LaRiojaBudgetLoader
else:
    from .larioja_budget_loader import LaRiojaBudgetLoader
