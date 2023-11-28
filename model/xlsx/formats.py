"""Formats for xlsx's cells"""


class Formats:

    merge_format_flip = {
        'font_size': 20,
        'border':    5,
        'align':     'center',
        'valign':    'vcenter',
        'rotation':  90
    }

    merge_format_back_flip = {
        'font_size': 20,
        'border':    5,
        'align':     'center',
        'valign':    'vcenter',
        'rotation': -90
    }

    merge_format = {
        'font_size': 15,
        'border':    5,
        'align':     'center',
        'valign':    'vcenter'
    }

    format_top_cell = {
        'font_size': 15,
        'top':       5,
        'left':      5,
        'right':     5,
        'align':     'center',
        'valign':    'vcenter'
    }

    format_mid_cell = {
        'font_size': 10,
        'top':       5,
        'left':      5,
        'right':     5,
        'align':     'center',
        'valign':    'vcenter'
    }

    format_bot_cell = {
        'font_size': 10,
        'bottom':    5,
        'left':      5,
        'right':     5,
        'align':     'center',
        'valign':    'vcenter'
    }

    @classmethod
    def get_merge_format_flip(cls):
        return cls.merge_format_flip.copy()

    @classmethod
    def get_merge_format_back_flip(cls):
        return cls.merge_format_back_flip.copy()

    @classmethod
    def get_merge_format(cls):
        return cls.merge_format.copy()

    @classmethod
    def get_format_top_cell(cls):
        return cls.format_top_cell.copy()

    @classmethod
    def get_format_mid_cell(cls):
        return cls.format_mid_cell.copy()

    @classmethod
    def get_format_bot_cell(cls):
        return cls.format_bot_cell.copy()

