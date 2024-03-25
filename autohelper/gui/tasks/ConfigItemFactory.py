from autohelper.gui.widget.ListTableWidgetItem import ListTableWidgetItem
from autohelper.gui.widget.NumericTableWidgetItem import NumericTableWidgetItem
from autohelper.gui.widget.YesNonWidgetItem import YesNonWidgetItem


def config_widget_item(table, row, col, config, key, value):
    if isinstance(value, bool):
        table.setCellWidget(row, 1, YesNonWidgetItem(config, key, value))
    elif isinstance(value, list):
        table.setItem(row, 1, ListTableWidgetItem(config, key, value))
    elif isinstance(value, (int, float)):
        table.setItem(row, 1, NumericTableWidgetItem(config, key, value))
    else:
        raise ValueError(f"invalid type {type(value)}")
