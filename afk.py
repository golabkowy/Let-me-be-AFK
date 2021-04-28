import win32con
import win32api as wapi
import win32gui as wgui
import win32process as wproc
import time
import math
from art import *


tprint("LET ME \nBE AFK!",font="starwars")
# xD
wapi.Beep(200,400)
wapi.Beep(300,400)
wapi.Beep(400,400)
wapi.Beep(500,400)

# ACTIVE WIDOWS STUFF
#wapi.SetCursorPos((50,50))


windows_arr = []
window_focus_name=""
afk_time =0
mouse_position_tuple = (0,0)

def display_opened_windows():
    local_windows_arr =[]
    local_windows_arr_filtered =[]
    def inner_callback_function(hwnd,extra):
        #hwnd - handler window
        local_windows_arr.append(wgui.GetWindowText(hwnd))
    
    wgui.EnumWindows(inner_callback_function,windows_arr)
    for w in local_windows_arr:
        if w != "Default IME" and w!= '' and w!= "MSCTFIME UI":
            local_windows_arr_filtered.append(w)
    print(local_windows_arr_filtered)

def set_window_to_focus_on():
    global window_focus_name
    #TODO check if window exist and test if works.
    window_focus_name = input("Insert window name or insert 'b' to return \n")

def set_afk_time():
    #TODO verify input
    global afk_time
    afk_time = int(input("Insert delay in seconds to activate afk mode. \n"))

# WINDOW
def set_focus_on_choosen_window():
    print("cokolwiek")
    print(window_focus_name)
    handle = wgui.FindWindow(None,window_focus_name)
    remote_thread, _ = wproc.GetWindowThreadProcessId(handle)
    wproc.AttachThreadInput(wapi.GetCurrentThreadId(), remote_thread, True)
    prev_handle = wgui.SetForegroundWindow(handle)#
    # it is possible to pass SW_MAX to maximize the window
    wgui.ShowWindow(handle, win32con.SW_SHOWNORMAL)
    prev_handle = wgui.SetFocus(handle)

# MOUSE
def calculate_mouse_cords(a,b,r,alfa):
    x_cord = (r * math.sin(math.radians(alfa))) + a
    y_cord = (r * math.cos(math.radians(alfa))) + b
    wapi.SetCursorPos((int(x_cord),int(y_cord)))
    #print("a: {} b: {} r: {} alfa: {} x_cord: {} y_cord: {}".format(a,b,r,alfa,int(x_cord),int(y_cord)))
    #get focused window center and draw by center
    
def is_mouse_same_position():
    global mouse_position_tuple
    if wgui.GetCursorInfo()[2][0] != mouse_position_tuple[0] or wgui.GetCursorInfo()[2][1] != mouse_position_tuple[1]:
        # NO AFK - user moved mouse recently
        mouse_position_tuple = (wgui.GetCursorInfo()[2][0],wgui.GetCursorInfo()[2][1])
        return False
    else:
        #AFK - same position for longer than specified time
        return True
        
def mouse_circulation():
    for i in range(0,360):
        calculate_mouse_cords(500,500,200,i)
        time.sleep(0.01)
        
def run_app():
    print("run app")
    while True:
        time.sleep(afk_time)
        print("timestamp")
        if is_mouse_same_position():
            set_focus_on_choosen_window()
            mouse_circulation()
                
def menu():
    dictionary = {
        1: display_opened_windows,
        2: set_window_to_focus_on,
        3: set_afk_time,
        4: run_app,
        5: exit
    }
    
    while True:
        display_menu_options()
        choosen_option = int(input())
        dictionary[choosen_option]()
    
def display_menu_options():
    print("\n")
    print("Tell me what to do: " + '\n')
    print("1 - Display currently opened windows.")
    print("2 - Set window to focuse on")
    print("3 - Set time to activate AFK mode")
    print("4 - Run it!")
    print("5 - Exit app")

        
############################## APP ENTRY POINT###########################
menu()

#TODO:

#verification of user inputs
#change size of active window
#set center of active window as a mouse circulation point
#set mouse circulation parameters from menu
#help
#refactor and clean up