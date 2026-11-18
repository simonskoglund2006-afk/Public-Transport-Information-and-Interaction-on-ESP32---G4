import lvgl as lv
import settings

MAX_RESULTS = 4      #temporarily

class GUI:
    'Builds and handles all screens on the display'
    def __init__(self, departures, stops, transport_types, departures_2):
        self.row_cells = []
        self.stop_buttons = []
        self.departures = departures
        self.departures_2 = departures_2
        self.transport_types = transport_types
        self.stops = stops
        self.selected_stop, self.selected_type = settings.load_settings(len(stops), len(transport_types))
        self.first_screen()
        self.second_screen()
        self.third_screen()
        
    @staticmethod
    def make_label(parent, text, y_offset):
        'Creates a centered black text label'
        label = lv.label(parent)
        label.set_text(text)
        label.set_style_text_font(lv.font_montserrat_28, 0)
        label.set_style_text_color(lv.color_hex(0x000000), 0)
        label.align(lv.ALIGN.TOP_MID, 0, y_offset)

        return label

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

    def add_cell(self, text, x, y, color=0x000000, track=False):
        'Adds one text cell to the departure screen'
        cell = lv.label(self.tile2)
        cell.set_text(text)
        cell.set_style_text_font(lv.font_montserrat_28, 0)
        cell.set_style_text_color(lv.color_hex(color), 0)
        cell.align(lv.ALIGN.TOP_LEFT, x, y)
        if track:
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
    
    def drop_down(self):
        'Creating drop down'
        heading = lv.label(self.tile3)
        heading.set_text('Transport type')
        heading.set_style_text_font(lv.font_montserrat_28, 0)
        heading.set_style_text_color(lv.color_hex(0x000000), 0)
        heading.align(lv.ALIGN.TOP_LEFT, 390, 72)

        self.type_dropdown = lv.dropdown(self.tile3)
        self.type_dropdown.set_options('\n'.join(self.transport_types))
        self.type_dropdown.set_selected(self.selected_type)
        self.type_dropdown.set_width(190)
        self.type_dropdown.align(lv.ALIGN.TOP_LEFT, 390, 105)
        self.type_dropdown.add_event_cb(
            self.on_type_changed, lv.EVENT.VALUE_CHANGED, None)

    def on_type_changed(self, _event):
        'Remembers the transport type picked in the dropdown'
        self.selected_type = self.type_dropdown.get_selected()
        self.draw_rows()

    def save_button(self):
        'Creating save button'   
        save = lv.button(self.tile3)
        save.set_size(190, 50)
        save.align(lv.ALIGN.TOP_LEFT, 390, 330)
        save.add_event_cb(self.saving_settings, lv.EVENT.CLICKED, None)

        save_label = lv.label(save)
        save_label.set_text('Save default')
        save_label.center()

        self.status_label = lv.label(self.tile3)
        self.status_label.set_text('')
        self.status_label.set_style_text_font(lv.font_montserrat_28, 0)
        self.status_label.set_style_text_color(lv.color_hex(0x000000), 0)
        self.status_label.align(lv.ALIGN.TOP_LEFT, 390, 390)

    def saving_settings(self, _event):
        'Saving current settings'
        ok = settings.save(self.selected_stop, self.selected_type)
        self.status_label.set_text('Saved' if ok else 'Save failed')

    def reset_settings(self):
        'Resetting settings back to default'
        self.selected_stop, self.selected_type = settings.load_settings(
            len(self.stops), len(self.transport_types))

        self.type_dropdown.set_selected(self.selected_type)
        self.search_box.set_text('')

        others = [i for i in range(len(self.stops)) if i != self.selected_stop]
        self.show_stops([self.selected_stop] + others)

        self.draw_rows()
        self.status_label.set_text('Restored')

    def build_restore_button(self):
        'Adds a button that restore the saved dafault settings'
        restore = lv.button(self.tile3)
        restore.set_size(190, 50)
        restore.align(lv.ALIGN.TOP_LEFT, 390, 270)
        restore.add_event_cb(self.on_restore_clicked, lv.EVENT.CLICKED, None)
        label = lv.label(restore)
        label.set_text('Restore')
        label.center()

    def on_restore_clicked(self, _event):
        'Runs the restore when teh button is tapped'
        self.reset_settings()

    def on_settings_clicked(self, _event):
        'Slides to the settings screen'
        self.tileview.set_tile(self.tile3, True)

    def draw_rows(self):
        'Redraws the departure rows for the selected stop and transport type'
        for cell in self.row_cells:
            cell.delete()
        self.row_cells = []

        name = self.stops[self.selected_stop]
        self.board_title.set_text(name)
        wanted = self.transport_types[self.selected_type]

        rows = [r for r in self.departures_2.get(name, [])
                if wanted == 'All' or r[4] == wanted]

        if not rows:
            self.add_cell('No departures', 20, 118, track=True)
        for row, (dep_time, line, dest, status, _kind) in enumerate(rows[:5]):
            y = 118 + row * 52
            color = 0x000000 if status == 'On time' else 0xCC0000
            self.add_cell(dep_time, 20, y, track=True)
            self.add_cell(line, 130, y, track=True)
            self.add_cell(dest, 250, y, track=True)
            self.add_cell(status, 470, y, color, track=True)

    def show_stops(self, indexes):
        'Replace the stop button on tile 3 with one button per given stop'
        for _index, button in self.stop_buttons:
            button.delete()
        self.stop_buttons = []
        for row, index in enumerate(indexes[:MAX_RESULTS]):
            button = lv.button(self.tile3)
            button.set_size(340, 46)
            button.align(lv.ALIGN.TOP_LEFT, 20, 125 + row * 52)
            button.add_event_cb(
                lambda _event, i=index: self.on_stop_clicked(i),
                lv.EVENT.CLICKED, None)
            label = lv.label(button)
            label.set_text(self.stops[index])
            label.set_style_text_font(lv.font_montserrat_28, 0)
            label.align(lv.ALIGN.LEFT_MID, 5, 0)
            self.stop_buttons.append((index, button))
        self.highlight_stop()

    def highlight_stop(self):
        'Colours the selcted stop green and others grey'
        for index, button in self.stop_buttons:
            colour = 0x1B5E20 if index == self.selected_stop else 0x7A869A
            button.set_style_bg_color(lv.color_hex(colour), 0)

    def on_stop_clicked(self, index):
        'Remembers the tapped stop, highlights it and updates the board'
        self.selected_stop = index
        self.highlight_stop()
        self.draw_rows()

    @staticmethod
    def to_ascii(text):
        'Plain-letter version of a name, so å/ä/ö can be searched as a/a/o'
        table = {"å": "a", "ä": "a", "ö": "o", "Å": "A", "Ä": "A", "Ö": "O"}
        return ''.join(table.get(ch, ch) for ch in text)

    def build_search(self):
        'Adds a seach box, results list and keyboard on tile 3'
        self.search_box = lv.textarea(self.tile3)
        self.search_box.set_one_line(True)
        self.search_box.set_placeholder_text('Seach stops')
        self.search_box.set_size(340, 46)
        self.search_box.align(lv.ALIGN.TOP_LEFT, 20, 72)
        self.search_box.add_event_cb(self.on_search_changed, lv.EVENT.VALUE_CHANGED, None)
        self.search_box.add_event_cb(self.on_search_focused, lv.EVENT.FOCUSED, None)

        self.keyboard = lv.keyboard(self.tile3)
        self.keyboard.set_textarea(self.search_box)
        self.keyboard.add_flag(lv.obj.FLAG.HIDDEN)
        self.keyboard.add_event_cb(self.on_keyboard_done, lv.EVENT.READY, None)
        self.keyboard.add_event_cb(self.on_keyboard_done, lv.EVENT.CANCEL, None)

        self.show_stops(list(range(len(self.stops))))

    def on_search_changed(self, _event):
        'Shows the stops whose name contains the typed text'
        query = self.to_ascii(self.search_box.get_text()).lower()
        matches = [i for i, name in enumerate(self.stops)
                   if query in self.to_ascii(name).lower()]
        self.show_stops(matches)

    def on_search_focused(self, _event):
        'Opens the keyboard when the search box is tapped'
        self.keyboard.remove_flag(lv.obj.FLAG.HIDDEN)
        self.keyboard.move_foreground()

    def on_keyboard_done(self, _event):
        'Hides the keyboard when the user taps the tick or close key'
        self.keyboard.add_flag(lv.obj.FLAG.HIDDEN)
    
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

        self.draw_rows()

        self.make_divider(self.tile2, 395)
        self.add_cell('Data from Trafiklab.se', 20, 406)
        self.add_setting_icon()

    def third_screen(self):
        'Settings screen'
        self.tile3.set_style_bg_color(lv.color_hex(0xFFFFFF), 0)
        self.tile3.set_style_bg_opa(lv.OPA.COVER, 0)
        self.build_search()
        self.drop_down()
        self.build_restore_button()
        self.save_button()
