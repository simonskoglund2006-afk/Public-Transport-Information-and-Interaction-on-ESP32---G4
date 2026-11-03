import lvgl as lv
<<<<<<< HEAD
import settings

class GUI:
    'Builds and handles all screens on the display'
    def __init__(self, departures, stops, transport_types):
        self.row_cells = []
        self.stop_buttons = []
        self.departures = departures
        self.stops = stops
        self.selected_stop, self.selected_type = settings.load_settings(len(stops), len(transport_types))
        self.first_screen()
        self.second_screen()
        self.third_screen()
        
=======


class GUI:
    'Builds and handles all screens on the display'

    def __init__(self, departures):
        self.departures = departures
        self.tile2_dark = False
        self.first_screen()
        self.second_screen()

>>>>>>> 0f40474 (created a new file and added my code there instead of main)
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

<<<<<<< HEAD
    @staticmethod
    def make_label(parent, text, y_offset):
        'Creates a centered black text label'
        label = lv.label(parent)
        label.set_text(text)
        label.set_style_text_font(lv.font_montserrat_28, 0)
        label.set_style_text_color(lv.color_hex(0x000000), 0)
        label.align(lv.ALIGN.TOP_MID, 0, y_offset)

        return label
=======
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
>>>>>>> 0f40474 (created a new file and added my code there instead of main)

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
<<<<<<< HEAD
        self.row_cells.append(cell)

    def add_setting_icon(self):
            'Adding a setting icon'
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
            gear.set_style_transform_scale(380, 0)
    
    def selecting_stops(self):
        'Selecting different stops'
        for index, name in enumerate(self.stops):
            button = lv.button(self.tite3)
            button.set_size(340, 46)
            button.align(lv.ALIGN.TOP_LEFT, 20, 80 + index * 52)
            button.add_event_cb(
                lambda _event, i= index: self.on_stop_clicked(i),
                lv.EVENT.CLICKED, None)

            label = lv.label(button)
            label.set_text(name)
            label.set_style_text_font(lv.font_montserrat_28, 0)
            label.align(lv.ALIGN.LEFT_MID, 5, 0)

            self.stop_buttons.append(button)
        self.highlight_stop()

    def highlight_stop(self):
        'Gives the user feedback'
        for index, button in enumerate(self.stop_buttons):
            colour = 0x1B5E20 if index == self.selected_stop else 0x7A869A
            button.set_style_bg_color(lv.color_hex(colour), 0)

    def on_stop_clicked(self, index):
        'Remembers the tapped stop and highlights it'
        self.selected_stop = index
        self.highlight_stop()
    
    def drop_down(self):
        'Creating drop down'
        pass

    def save_button(self):
        'Creating save button'   
        save = lv.button(self.tile3)
        save.set_size(190, 50)
        save.align(lv.ALIGN.TOP_LEFT, 390, 330)
        save.add_event_cb(self.on_save_clicked, lv.EVENT.CLICKED, None)

        save_label = lv.label(save)
        save_label.set_text('Save default')
        save_label.center()

        self.status_label = lv.label(self.tile3)
        self.status_label.set_text('')
        self.status_label.set_style_text_font(lv.font_montserrat_28, 0)
        self.status_label.set_style_text_color(lv.color_hex(0x000000), 0)
        self.status_label.align(lv.ALIGN.TOP_LEFT, 390, 390)

    def saving_settings(self):
        'Saving current settings'
        ok = settings.save(self.selected_stop, self.selected_type)
        self.status_label.set_text('Saved' if ok else 'Save failed')

    def reset_settings(self):
        'Resetting settings back to default'
        pass

    def on_settings_clicked(self, _event):
        'Slides to the settings screen'
        self.tileview.set_tile(self.tile3, True)
    
    def first_screen(self):
        'Introduction screen'
        self.tileview = lv.tileview(lv.screen_active())
        self.tileview.set_size(600, 450)
        self.tileview.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
        self.tileview.set_style_bg_color(lv.color_hex(0xFFFFFF), 0)
        self.tileview.set_style_bg_opa(lv.OPA.COVER, 0)

        self.tile1 = self.tileview.add_tile(0, 0, lv.DIR.RIGHT)
        self.tile2 = self.tileview.add_tile(1, 0, lv.DIR.LEFT)
        self.tile3 = self.tileview.add_tile(2, 0, lv.DIR.LEFT)

        self.title_label = self.make_label(self.tile1, "Public Transport Information", 20)
        self.version_label = self.make_label(self.tile1, "V2", 70)
        self.group_label = self.make_label(self.tile1, "Group 4", 110)
        self.names_label = self.make_label(self.tile1, "Albin Persson\nDaniel Ojog\nFelix Rudiger\nLucas Jonsson\nSimon Skoglund", 150)         #Unfortunally I can not find a way to write åäö :(

        self.tile1.set_style_bg_color(lv.color_hex(0xFFFFFF), 0)
        self.tile1.set_style_bg_opa(lv.OPA.COVER, 0)
=======
>>>>>>> 0f40474 (created a new file and added my code there instead of main)

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
<<<<<<< HEAD
        self.add_setting_icon()

    def third_screen(self):
        'Settings screen'
        self.tile3.set_style_bg_color(lv.color_hex(0xFFFFFF), 0)
        self.tile3.set_style_bg_opa(lv.OPA.COVER, 0)
        self.selecting_stops()
        self.save_button()
    
=======

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
>>>>>>> 0f40474 (created a new file and added my code there instead of main)
