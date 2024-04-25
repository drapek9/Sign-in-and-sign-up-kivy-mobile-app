all_screens = ["choose way"]
def append_previous_screen(new_screen):
    global all_screens
    if new_screen == "choose way":
        all_screens = ["choose way"]
        print(all_screens)
    else:
        all_screens.append((new_screen))
# Function for bigger or smaller title
def check_width_function(self):
        if self.width > 1200:
            per = 0.04
            b = .3
        elif self.width > 1000:
            per = 0.08
            b = .5
        else:
            per = 0.09
            b = .6
        self.num_for_x = self.width * per
        self.but_pos_x_hint = b

def previous_screen():
        global all_screens
        if len(all_screens):
            all_screens = all_screens[:-1]
            previous_screen_name = all_screens[-1]
            print(all_screens)
            return previous_screen_name