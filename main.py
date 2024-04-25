from kivy.config import Config
Config.set("graphics", "width", "360")
Config.set("graphics", "height", "740")
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition, FadeTransition, WipeTransition, NoTransition, CardTransition
from kivy.properties import NumericProperty, StringProperty, Clock, ObjectProperty, BooleanProperty, ListProperty
import ast
from kivy.graphics import Color, Line
from kivy.core.audio import SoundLoader
from datetime import datetime
import pytz

# IN THIS PROJECT, IM NOT USING KIVYMD, BUT AFTER THIS PROJECT, I STARTED USING IT

# from kivymd.app import MDApp

# from functions_for_all_class import append_previous_screen, check_width_function, previous_screen, all_screens

# with open("files/users.txt", "r+") as file:
#     d = file.read()
#     r = ast.literal_eval(d)

#     new_dict = {"dada123": {"name":"David Jirsák", "password": "123dada123"}}
#     r.update(new_dict)
#     file.truncate()

# with open("files/users.txt", "w") as file_2:
#     file_2.write(str(r))
#     file_2.close()

all_screens = ["choose way"]
def append_previous_screen(new_screen):
    global all_screens
    if new_screen == "choose way":
        all_screens = ["choose way"]
    else:
        all_screens.append((new_screen))
# Function for bigger or smaller title
def check_width_function(self):
        print(self.width)
        if self.width > 2000:
            per = 0.04
            b = .25
            bs = .15
            l = .45
            l2 = .4
            s = .25
        elif self.width > 1400:
            per = 0.06
            b = .3
            bs = .2
            l = .5
            l2 = .45
            s = .35
        elif self.width > 1000:
            per = 0.07
            b = .5
            bs = .2
            l = .65
            l2 = .55
            s = .45
        else:
            per = 0.09
            b = .6
            bs = .3
            l = .65
            l2 = .55
            s = .5
        self.num_for_x = self.width * per
        self.but_pos_x_hint = b
        try:
            self.buttons_width_hint = bs
        except:
            pass
        try:
            self.line_width = l
        except:
            pass
        try:
            self.line_width_2 = l2
        except:
            pass
        try:
            self.slider_width = s
        except:
            pass

def previous_screen():
        global all_screens
        if len(all_screens):
            all_screens = all_screens[:-1]
            previous_screen_name = all_screens[-1]
            # print(all_screens)
            return previous_screen_name

the_message = "HBdhebbcrrbviuv"
new_user_message = "Trying to signup"
old_user_message = "Trying to sign in"
# We need it, because we have to call function on_size and we cant get the properties
name_now = None
username_now = None
password_now = None
num_of_space_in_name = 0
num_of_dash = 0

class ChooseWay(Screen):
    but_pos_x_hint = NumericProperty(.55)
    num_for_x = NumericProperty(20)
    buttons_width_hint = NumericProperty(.2)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def on_pre_enter(self):
        self.sign_up.reset_names()
        self.sign_in.reset_sign_in_names()
    def on_size(self, *kwargs):
        check_width_function(self)
        # print(self.width)

    def change_screen_on_sign_in(self):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "sign in"
    def change_screen_on_sign_up(self):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "sign up"
    def on_keyboard(self, window, keycode, scancode, codepoint, modifiers):
        if keycode == 27:
            self.main_class.stop()

class BetweenScreens(Screen):
    menu_button = ObjectProperty()
    main_text = StringProperty(the_message)
    name_for_app = ""
    def __init__(self, **kw):
        super().__init__(**kw)
    def on_pre_enter(self):
        self.menu_button.opacity = 0
        append_previous_screen("between")
        # if it would be on servers, we would have to add text like "wait" and than when it would be ready, we call on_control_users
        if the_message == new_user_message:
            global name_now, username_now, password_now
            self.on_control_users(name_now, username_now, password_now)
        if the_message == old_user_message:
            self.on_sign_in(self.sign_in.username2.text, self.sign_in.password2.text)

    # def on_size(self, *kwargs):
    #     self.main_text = the_message
    def change_the_manager(self, dt):
        the = previous_screen()
        self.clo.cancel()
        self.manager.transition = FadeTransition()
        self.manager.current = the

    def on_control_users(self, namik, usernamik, passwordik):
        global the_message
        if self.check_users(usernamik):
            with open("files/users.txt", "r+") as file:
                d = file.read()
                r = ast.literal_eval(d)

                new_dict = {usernamik: {"name" : namik, "password" : passwordik, "age": int(self.sign_up.slider_numeric.value)}}
                r.update(new_dict)
                file.truncate()

            with open("files/users.txt", "w") as file_2:
                file_2.write(str(r))
                file_2.close()
            
            the_message = "Your registration was successful :)"
            self.main_text = the_message
            self.menu_button.opacity = 1

        else:
            the_message = "Your account already exist!"
            self.main_text = the_message
            self.clo = Clock.schedule_interval(self.change_the_manager, 3)

    def check_users(self, usernam):
        with open("files/users.txt", "r") as file:
           d = file.read()
           r = ast.literal_eval(d)
        
        if usernam in r.keys():
            return False
        else:
            return True
        
    def back_to_menu(self):
        global all_screens
        if self.menu_button.opacity == 1:
            all_screens = ["choose way"]
            self.manager.current = "choose way"
    
    def on_sign_in(self, name, password):
        if self.control_username(name):
            if self.control_password(name, password):
                the_message = ""
                self.sign_in.reset_sign_in_names()
                self.main_text = the_message
                self.manager.transition = CardTransition()
                self.manager.current = "application"

            else:
                the_message = "You have written bad account or bad password!"
                self.main_text = the_message
                self.clo = Clock.schedule_interval(self.change_the_manager, 3)
        else:
            the_message = "You have written bad account or bad password!"
            self.main_text = the_message
            self.clo = Clock.schedule_interval(self.change_the_manager, 3)

    def control_username(self, name):
        with open("files/users.txt", "r") as file:
            d = file.read()
            self.r = ast.literal_eval(d)
        
        if name in self.r.keys():
            self.username_with_name = name
            return True
        return False

    def control_password(self, name, password):
        if self.r[name]["password"] == password:
            self.name_for_app = self.r[name]["name"]
            return True
        return False

class SignUp(Screen):
    line_id = ObjectProperty(None)
    his_name = ObjectProperty(None)
    username = ObjectProperty(None)
    password = ObjectProperty(None)
    confirmpassword = ObjectProperty(None)

    line_width_2 = NumericProperty(.6)

    button_disabled = BooleanProperty()

    slider_numeric = ObjectProperty(None)
    max_age_lenght = 3

    error_clock = None
    num_for_x = NumericProperty(20)
    y_size_hint = NumericProperty(.045)
    x_size_hint = NumericProperty(.6)
    y_pos_hint = NumericProperty(.7)
    x_pos_hint = NumericProperty(.5)
    but_pos_x_hint = NumericProperty(.55)
    diff_y = NumericProperty(.1)
    # hal - left/center/right
    # val - auto/top/middle/bottom
    hal = StringProperty("left")
    val = StringProperty("middle")
    name_title = StringProperty("Name")
    username_title = StringProperty("Username")
    pass_title = StringProperty("Password")
    confirm_pass_title = StringProperty("Confirm password")
    error_text = StringProperty("")
    name_user_number_min = NumericProperty(5)
    user_number_max = NumericProperty(13)
    name_number_max = NumericProperty(20)
    pass_number_min = NumericProperty(8)
    pass_number_max = NumericProperty(15)

    slider_width = NumericProperty(.5)
    
    with open("files/allowed_letters.txt", "r", encoding="utf-8") as file:
        d = file.read()
        s = ast.literal_eval(d)
    allowed_letters = s

    # for correct showing label
    num_of_space = NumericProperty(num_of_space_in_name)
    num_of_dashnik = NumericProperty(num_of_dash)

    def __init__(self, **kw):
        super().__init__(**kw)
    def on_pre_enter(self):
        global all_screens
        # print(all_screens)
        if all_screens[-1] != "sign up":
            append_previous_screen("sign up")

    def control_age_len(self, age_input):
        if self.max_age_lenght < len(age_input.text):
            age_input.text = age_input.text[:self.max_age_lenght]
        if age_input.text == "":
            self.clock_wait = Clock.schedule_interval(lambda dt: self.on_clock_wait(age_input, dt), 2.3)
    def on_clock_wait(self, age_input, dt):
        if age_input.text == "":
            age_input.text = "0"
        self.clock_wait.cancel()

    def on_set_age(self, age_input):
        if age_input.text == "":
            age_input.text = "0"
        if int(age_input.text) <= self.slider_numeric.max:
            self.slider_numeric.value = age_input.text
        else:
            age_input.text = str(int(self.slider_numeric.value))
    def on_size(self, *kwargs):
        check_width_function(self)
        
    def sign_in_error_button_start_clock(self, error_name):
        self.error_text = error_name
        try:
            self.error_clock.cancel()
        except:
            pass
        self.error_clock = Clock.schedule_interval(self.sign_in_error_button_cancel, 3)
    def sign_in_error_button_cancel(self, dt):
        self.error_clock.cancel()
        self.error_text = ""
    
    def reset_names(self):
        self.his_name.text = "Name"
        self.username.text = "Username"
        self.confirmpassword.text = "Confirm password"
        self.password.text = "Password"
        for one_name in [self.his_name, self.username, self.password, self.confirmpassword]:
            one_name.foreground_color = "grey"
        self.slider_numeric.value = 0

    def check_len(self, minimal, maximal, the_text):
        global num_of_space_in_name, num_of_dash
        self.num_of_space = num_of_space_in_name
        self.num_of_dashnik = num_of_dash

        if maximal == self.name_number_max:
            num_of_space_in_name = the_text.text.count(" ")
            num_of_dash = the_text.text.count("-")
            self.num_of_space = num_of_space_in_name
            self.num_of_dashnik = num_of_dash
        else:
            self.num_of_dashnik = 0
            self.num_of_space = 0
        if maximal == self.name_number_max:
            the_symbols_dont_want = ["  ", "--", "- -"]
            the_symbols_i_want = list(self.allowed_letters) + [" " , "-"]
            list_text = list(the_text.text)
            list_text.reverse()
            if num_of_space_in_name > 2 and "  " not in the_text.text:
                del list_text[list_text.index(" ")]
            if num_of_dash > 2 and "--" not in the_text.text:
                del list_text[list_text.index("-")]
            list_text.reverse()
            the_text.text = "".join(list_text)
            try:
                if the_text.text[0] == " ":
                    the_text.text = the_text.text[1:]
            except:
                pass
        else:
            the_symbols_dont_want = [" "]
            the_symbols_i_want = list(self.allowed_letters) + ["-" , "_" , ".", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        for symbol in the_symbols_dont_want:
            if symbol in the_text.text and the_text.focus:
                the_text.text = the_text.text.replace(symbol, "")
        for letter in the_text.text:
            if letter not in the_symbols_i_want and the_text.focus:
                the_text.text = the_text.text.replace(letter, "")

        if len(the_text.text) >= minimal + self.num_of_space + self.num_of_dashnik and len(the_text.text) <= maximal + self.num_of_space + self.num_of_dashnik:
            the_text.foreground_color = "green"
        else:
            the_text.foreground_color = "red"
        if self.name_number_max >= len(self.his_name.text) - self.num_of_space - self.num_of_dashnik >= self.name_user_number_min \
        and self.user_number_max >= len(self.username.text) >= self.name_user_number_min and self.pass_number_max >= len(self.password.text) >= self.pass_number_min \
        and self.pass_number_max >= len(self.confirmpassword.text) >= self.pass_number_min and self.his_name.text != self.name_title \
        and self.username.text != self.username_title and self.password.text != self.pass_title and self.confirmpassword.text != self.confirm_pass_title:
            self.button_disabled = False
        else:
            self.button_disabled = True

    def check_text_input_un_click_click(self, the_input, the_name):
        text_input = the_input.text
        if text_input == the_name:
            the_input.text = ""
        if (text_input == "" or text_input == the_name) and the_input.focus == False:
            the_input.text = the_name
            the_input.foreground_color = "grey"

    def sign_up_button(self, sign_up_name, sign_up_username, sign_up_password, sign_up_confirm_password):
        global name_now, username_now, password_now
        name_now = sign_up_name.text
        username_now = sign_up_username.text
        password_now = sign_up_password.text
        conf_password = sign_up_confirm_password.text

        if (name_now not in (self.name_title, "")) and (username_now not in (self.username_title, "")) and (password_now not in (self.pass_title, "")) and (conf_password not in (self.confirm_pass_title, "")):
            if self.slider_numeric.value >= 15:
                if password_now == conf_password:
                    global the_message
                    the_message = new_user_message
                    # self.manager.transition = SlideTransition("right")
                    self.manager.transition = FadeTransition()
                    self.manager.current = "between"
                else:
                    self.sign_in_error_button_start_clock("Password and conform password doesn't match")
            else:
                self.sign_in_error_button_start_clock("Oops! You're too young for our app.")
        else:
            self.sign_in_error_button_start_clock("You have not entered all the data!")
    def back_on_screen(self):
        self.ids.the_sign_up_back_image.source = "images/back_pressed.png"
    def back_on_screen_release(self):
        self.ids.the_sign_up_back_image.source = "images/back.png"
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = previous_screen()
    
    # It should go on previous screen, if user click on button back on android
    def on_keyboard(self, window, keycode, scancode, codepoint, modifiers):
        if keycode == 27:
            self.manager.current = previous_screen()


class SignIn(Screen):
    username2 = ObjectProperty()
    password2 = ObjectProperty()
    button_disabled = BooleanProperty(True)

    pass_number_min = NumericProperty(8)
    pass_number_max = NumericProperty(15)

    name_user_number_min = NumericProperty(5)
    name_user_number_max = NumericProperty(13)

    but_pos_x_hint = NumericProperty(.3)
    line_width = NumericProperty(.55)

    y_size_hint = NumericProperty(.045)
    x_size_hint = NumericProperty(.6)
    y_pos_hint = NumericProperty(.62)
    x_pos_hint = NumericProperty(.5)
    diff_y = NumericProperty(.15)
    num_for_x = NumericProperty(20)
    hal2 = StringProperty("left")
    val2 = StringProperty("middle")
    name_user_title = StringProperty("Username")
    pass_title = StringProperty("Password")
    def __init__(self, **kw):
        super().__init__(**kw)
    def on_size(self, *kwargs):
        check_width_function(self)
    def on_pre_enter(self):
        global all_screens
        if all_screens[-1] != "sign in":
            append_previous_screen("sign in")
    def check_text_input_un_click_click_2(self, the_input2, the_name2):
        text_input = the_input2.text
        if text_input == the_name2:
            the_input2.text = ""
            the_input2.foreground_color = "black"
        if (text_input == "" or text_input == the_name2) and the_input2.focus == False:
            the_input2.text = the_name2
            the_input2.foreground_color = "white"
    def sign_in_button(self):
        global the_message, username_now, password_now, name_now
        if self.password2.text not in (self.pass_title, "") and self.username2 not in (self.name_user_title, ""):
            the_message = old_user_message
            username_now = self.username2.text
            password_now = self.password2.text
            with open("files/users.txt", "r") as file:
                r = file.read()
                s = ast.literal_eval(r)
            name_now = s[username_now]["name"]
            self.manager.transition = FadeTransition()
            self.manager.current = "between"
    
    def reset_sign_in_names(self):
        self.username2.text = self.name_user_title
        self.password2.text = self.pass_title

        for one_thing in [self.username2, self.password2]:
            one_thing.foreground_color = "white"
    
    def on_write_text_input(self, minimal, maximal, the_text):
        if maximal >= len(the_text.text) >= minimal:
            the_text.foreground_color = "green"
        else:
            the_text.foreground_color = "red"
        
        if self.pass_number_max >= len(self.password2.text) >= self.pass_number_min and self.name_user_number_max >= len(self.username2.text) >= self.name_user_number_min and self.username2.text != self.name_user_title and self.password2.text != self.pass_title:
            self.button_disabled = False
        else:
            self.button_disabled = True

    def back_on_screen_2(self):
        self.ids.the_sign_in_back_image.source = "images/back_pressed.png"
    def back_on_screen_release_2(self):
        self.ids.the_sign_in_back_image.source = "images/back.png"
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = previous_screen()
    
    # It should go on previous screen, if user click on button back on android
    def on_keyboard(self, window, keycode, scancode, codepoint, modifiers):
        if keycode == 27:
            self.manager.current = previous_screen()

class TheAppScreen(Screen):
    main_title = StringProperty()
    def __init__(self, **kw):
        super().__init__(**kw)
    def on_pre_enter(self):
        self.main_title = f"{self.between.name_for_app}"
        self.the_song = SoundLoader.load("music/application_song.mp3")
        self.the_song.loop = True
        Clock.schedule_interval(self.on_get_time, 1)
        print(f"name: {name_now}")
        print(f"username: {username_now}")
        print(f"password: {password_now}")
        with open("files/signed_user.txt", "w") as file:
            file.write(str({username_now: {"name": name_now, "password": password_now}}))
        # self.the_song.play()
    def on_get_time(self, dt):
        tz = pytz.timezone("Europe/Prague")
        current_time = datetime.now(tz)
        self.ids.time_label.text = f"Čas: {current_time.strftime("%X")}"
    def sign_out(self):
        self.delete_from_signed()
        append_previous_screen("choose way")
        self.manager.transition = FadeTransition()
        self.manager.current = "choose way"
    
    def on_keyboard(self, window, keycode, scancode, codepoint, modifiers):
        if keycode == 27:
            self.main_class.stop()
    # In future, i will ask if he is sure Yes/No
    def cancel_account(self):
        self.delete_from_signed()
        with open("files/users.txt", "r") as file:
            s = file.read()
            data = ast.literal_eval(s)
        global username_now
        print(username_now)
        del data[username_now]
        with open("files/users.txt", "w") as file:
            file.write(str(data))
        append_previous_screen("choose way")
        self.manager.transition = FadeTransition()
        self.manager.current = "choose way"
    def delete_from_signed(self):
        with open("files/signed_user.txt", "w") as file:
            pass

class MyApp(App):
    def build(self):
        self.sm = ScreenManager()
        # self.choose_way = ChooseWay(self.sign_up, self.sign_in, self.between)
        # self.sign_up = SignUp(self.choose_way, self.sign_in, self.between)
        # self.sign_in = SignIn(self.choose_way, self.sign_up, self.between)
        # self.between = Between_screens(self.choose_way, self.sign_up, self.sign_in)

        # We need it for change the names and more
        # We just added the classes to another class 5 times

        # Window.fullscreen = "auto"

        self.choose_way = ChooseWay()
        self.sign_up = SignUp() 
        self.sign_in = SignIn()
        self.between = BetweenScreens()
        self.the_application = TheAppScreen()

        self.choose_way.sign_up = self.sign_up
        self.choose_way.sign_in = self.sign_in
        self.choose_way.between = self.between
        self.choose_way.the_app = self.the_application
        self.choose_way.main_class = self

        self.sign_up.choose_way = self.choose_way
        self.sign_up.sign_in = self.sign_in
        self.sign_up.between = self.between
        self.sign_up.the_app = self.the_application
        self.sign_up.main_class = self

        self.sign_in.choose_way = self.choose_way
        self.sign_in.sign_up = self.sign_up
        self.sign_in.between = self.between
        self.sign_in.the_app = self.the_application
        self.sign_in.main_class = self
        
        self.between.choose_way = self.choose_way
        self.between.sign_up = self.sign_up
        self.between.sign_in = self.sign_in
        self.between.the_app = self.the_application
        self.between.main_class = self

        self.the_application.choose_way = self.choose_way
        self.the_application.sign_up = self.sign_up
        self.the_application.sign_in = self.sign_in
        self.the_application.between = self.between
        self.the_application.main_class = self

        for one_class in [self.choose_way, self.sign_in, self.sign_up, self.between, self.the_application]:
            self.sm.add_widget(one_class)
        # sign up, sign in, choose way, between, application
        try:
            with open("files/signed_user.txt", "r") as file:
                r = file.read()
                s = ast.literal_eval(r)
                global name_now, password_now, username_now
                username_now = s.keys()
                for one in username_now:
                    username_now = one
                name_now = s[username_now]["name"]
                username_now = s[username_now]["name"]
                self.sm.current = "application"
                append_previous_screen("application")
        except:
            self.sm.current = "choose way"
            append_previous_screen("choose way")

        return self.sm
    def on_stop(self):
        print("bey")

if __name__ == "__main__":
    MyApp().run()