
preview_redraw = False
main_redraw = False

rendering_frequency = 1000
leather_path_list = ["G:\hdsk", "G:\hd", "G:\hd-arch"]
domyslne_leather_path = 1
leather_backup_path = "G:\\Kontrola_skanerow_backup"

#barcode scanner
barcode_com_port = "COM3"

#hand follower options
camera_res_width = 1920
camera_res_height = 1080
camera_frames = 30
camera_port_number = 1
#kalman
#wariacja_x = 0.563819203
#wariacja_y = 0.733453408
wariacja_x = 1
wariacja_y = 1

Pc_x = 0
G_x = 0
P_x = 1
Xp_x = 0
Zp_x = 0
Xe_x = 0

Pc_y = 0
G_y = 0
P_y = 1
Xp_y = 0
Zp_y = 0
Xe_y = 0

wsp_kal = 0.1

#AI
tracking_confidence = 0.8
detection_confidence = 0.8
model_complex = 0

cursor_radius = 5
cursor_color = (255,255,0)

flaw_dropdown_menu_x_size = 120
flaw_dropdown_menu_y_size = 75
flaw_dropdown_menu_color = (245, 65, 230)
flaw_dropdown_menu_option_color = (185, 0, 174)
flaw_dropdown_menu_font_color = (65, 245, 80)
flaw_dropdown_menu_options = ['Warstwa', 'Usuń', 'Przesuń']
flaw_dropdown_layer_menu_options = ['Niebieska', 'Zielona', 'Żółta', 'Czerwona']
flaw_dropdown_menu_options_amount = len(flaw_dropdown_menu_options)

dropdown_menu_x_size = 130
dropdown_menu_y_size = 30
dropdown_menu_color = (152, 12, 243)
dropdown_menu_option_color = (90, 0, 185)
dropdown_menu_font_color = (103, 243, 12)
dropdown_menu_options = ['Rysuj skaze']
dropdown_menu_options_amount = len(dropdown_menu_options)

open_flaw_line_width = 3
new_flaw_color = (255,255,255)
c_layer_line_width = 1
new_flaw_line_width = 1
flaw_line_width = 1

bg_layer_color = (0, 0, 0)
c_layer_color = (255, 255, 255)
h_layer_color = (127, 127, 127)
h_layer_linetype = 'polygon'
b_layer_color = (0, 0, 255)
b_layer_linetype = 'polygon'
g_layer_color = (0, 255, 0)
g_layer_linetype = 'polygon'
y_layer_color = (255, 255, 0)
y_layer_linetype = 'polygon'
r_layer_color = (255, 0, 0)
r_layer_linetype = 'polygon'

first_bg_layer_color = (0, 0, 0)
first_c_layer_color = (255, 255, 255)
first_h_layer_color = (127, 127, 127)
first_h_layer_linetype = 'polygon'
first_b_layer_color = (0, 0, 255)
first_b_layer_linetype = 'polygon'
first_g_layer_color = (0, 255, 0)
first_g_layer_linetype = 'polygon'
first_y_layer_color = (255, 255, 0)
first_y_layer_linetype = 'polygon'
first_r_layer_color = (255, 0, 0)
first_r_layer_linetype = 'polygon'

second_bg_layer_color = (0, 0, 0)
second_c_layer_color = (255, 255, 255)
second_h_layer_color = (127, 127, 127)
second_h_layer_linetype = "lines"
second_b_layer_color = (0, 0, 255)
second_b_layer_linetype = "lines"
second_g_layer_color = (0, 255, 0)
second_g_layer_linetype = "lines"
second_y_layer_color = (255, 255, 0)
second_y_layer_linetype = "lines"
second_r_layer_color = (255, 0, 0)
second_r_layer_linetype = "lines"

h_layer_flag = True
b_layer_flag = True
g_layer_flag = True
y_layer_flag = True
r_layer_flag = True
