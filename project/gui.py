import lvgl as lv


class GUI:
    'Builds and handles all screens on the display'

    def __init__(self, departures):
        self.departures = departures
        self.tile2_dark = False
        self.first_screen()
        self.second_screen()

    @staticmethod
    def apply_tile_colors(tile, label, dark):
        tile.set_style_bg_opa(lv.OPA.COVER, 0)
        tile.set_style_bg_color(
            lv.color_hex(0x000000 if dark else 0xFFFFFF), 0
        )
        label.set_style_text_color(
            lv.color_hex(0xFFFFFF if dark else 0x000000), 0
        )

    def on_tile2_clicked(self, _event):
        self.tile2_dark = not self.tile2_dark
        self.apply_tile_colors(self.tile2, self.board_title, self.tile2_dark)

    def first_screen(self):
        'First screen'
        self.tileview = lv.tileview(lv.screen_active())
        self.tileview.set_size(600, 450)
        self.tileview.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
        self.tileview.set_style_bg_color(lv.color_hex(0xFFFFFF), 0)
        self.tileview.set_style_bg_opa(lv.OPA.COVER, 0)

        self.tile1 = self.tileview.add_tile(0, 0, lv.DIR.RIGHT)
        self.tile2 = self.tileview.add_tile(1, 0, lv.DIR.LEFT)
        self.tile3 = self.tileview.add_tile(2, 0, lv.DIR.LEFT)

        self.title_label = lv.label(self.tile1)
        self.title_label.set_text("Public Transport Information")
        self.title_label.set_style_text_font(lv.font_montserrat_28, 0)
        self.title_label.align(lv.ALIGN.TOP_MID, 0, 20)
        self.title_label.set_style_text_color(lv.color_hex(0x000000), 0)

        self.version_label = lv.label(self.tile1)
        self.version_label.set_text("V2")
        self.version_label.set_style_text_font(lv.font_montserrat_28, 0)
        self.version_label.align(lv.ALIGN.TOP_MID, 0, 70)
        self.version_label.set_style_text_color(lv.color_hex(0x000000), 0)

        self.group_label = lv.label(self.tile1)
        self.group_label.set_text("Group 4")
        self.group_label.set_style_text_font(lv.font_montserrat_28, 0)
        self.group_label.align(lv.ALIGN.TOP_MID, 0, 110)
        self.group_label.set_style_text_color(lv.color_hex(0x000000), 0)

        self.names_label = lv.label(self.tile1)
        self.names_label.set_text("Albin Persson\nDaniel Ojog\nFelix Rudiger\nLucas Jonsson\nSimon Skoglund")         #Unfortunally I can not find a way to write åäö :(
        self.names_label.set_style_text_font(lv.font_montserrat_28, 0)
        self.names_label.align(lv.ALIGN.TOP_MID, 0, 150)
        self.names_label.set_style_text_color(lv.color_hex(0x000000), 0)

        self.tile1.set_style_bg_color(lv.color_hex(0xFFFFFF), 0)
        self.tile1.set_style_bg_opa(lv.OPA.COVER, 0)

    @staticmethod
    def make_divider(parent, y_offset, width=560):
        'Draws a thin horizontal line'
        line = lv.obj(parent)
        line.set_size(width, 2)
        line.set_style_bg_color(lv.color_hex(0x000000), 0)
        line.set_style_bg_opa(lv.OPA.COVER, 0)
        line.set_style_border_width(0, 0)
        line.set_style_radius(0, 0)
        line.align(lv.ALIGN.TOP_MID, 0, y_offset)

        return line

    def add_cell(self, text, x, y, color=0x000000):
        'Adds one text cell to the departure screen'
        cell = lv.label(self.tile2)
        cell.set_text(text)
        cell.set_style_text_font(lv.font_montserrat_28, 0)
        cell.set_style_text_color(lv.color_hex(color), 0)
        cell.align(lv.ALIGN.TOP_LEFT, x, y)

    def second_screen(self):
        'Departure screen'
        self.tile2.set_style_bg_color(lv.color_hex(0xFFFFFF), 0)
        self.tile2.set_style_bg_opa(lv.OPA.COVER, 0)

        self.board_title = lv.label(self.tile2)
        self.board_title.set_text('Departures')
        self.board_title.set_style_text_font(lv.font_montserrat_28, 0)
        self.board_title.set_style_text_color(lv.color_hex(0x000000), 0)
        self.board_title.align(lv.ALIGN.TOP_MID, 0 , 15)
        self.make_divider(self.tile2, 60)

        self.add_cell('Time', 20, 72)
        self.add_cell('Line', 130, 72)
        self.add_cell('Destination', 250, 72)
        self.add_cell('Status', 470, 72)
        self.make_divider(self.tile2, 107)

        for row, (dep_time, line, dest, status) in enumerate(self.departures):
            y = 118 + row * 52
            color = 0x000000 if status == 'On time' else 0xCC0000
            self.add_cell(dep_time, 20, y)
            self.add_cell(line, 130, y)
            self.add_cell(dest, 250, y)
            self.add_cell(status, 470, y, color)

        self.make_divider(self.tile2, 395)
        self.add_cell('Data from Trafiklab.se', 20, 406)

        self.add_setting_icon()

    def add_setting_icon(self):
        'adding a setting icon'
        self.settings_btn = lv.button(self.tile2)
        self.settings_btn.set_size(50, 50)
        self.settings_btn.align(lv.ALIGN.TOP_RIGHT, -10, 5)
        self.settings_btn.add_event_cb(self.on_settings_clicked, lv.EVENT.CLICKED, None)

        gear = lv.label(self.settings_btn)
        gear.set_text(lv.SYMBOL.SETTINGS)
        gear.set_style_text_font(lv.font_montserrat_28, 0)
        gear.center()

        gear.update_layout()
        gear.set_style_transform_pivot_x(gear.get_width() // 2, 0)
        gear.set_style_transform_pivot_y(gear.get_height() // 2, 0)
        gear.set_style_transform_scale(384, 0)

    def on_settings_clicked(self, _event):
        'Slides to the settings screen'
        self.tileview.set_tile(self.tile3, True)
