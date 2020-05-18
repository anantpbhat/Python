#!/usr/bin/env python

from openpyxl import load_workbook
from openpyxl.styles import Font, colors
from openpyxl.formatting.rule import ColorScaleRule

xlfile = "firstxl.xlsx"
colorscalerule = ColorScaleRule(start_type="num", start_value=-5, start_color=colors.GREEN,
                                mid_type="num", mid_value=0, mid_color=colors.YELLOW,
                                end_type="num", end_value=5, end_color=colors.RED)

wb = load_workbook(filename=xlfile)
sheet = wb.active
sheet.conditional_formatting.add('D2:D11', colorscalerule)
wb.save(filename=xlfile)