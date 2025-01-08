import PySimpleGUI as sg
import serial
import json
import csv
import time

sg.theme('Purple')

## Win
#ser = serial.Serial('COM6', 115200)

## Linux
#ser = serial.Serial('/dev/ttyUSB0', 115200)
ser = serial.Serial('/dev/ttyACM0', 115200)


#フレーム定義
#ラベル表示フレーム
frame_Label = sg.Frame('',
        [
            [sg.Button('I',size=(20,50)),
             sg.Button('J',size=(20,50)), 
             sg.Button('K',size=(20,50)), 
             sg.Button('L',size=(20,50)), 
             sg.Button('M',size=(20,50))]
        ]
        , size = (1000, 50))

#変位表示フレーム
frame_Disp = sg.Frame('', 
        [
            
            [sg.Text('ローカル変位')],
            [
             sg.MLine(size=(20,100), key='-ML_I-'),
             sg.MLine(size=(20,100), key='-ML_J-'),
             sg.MLine(size=(20,100), key='-ML_K-'),
             sg.MLine(size=(20,100), key='-ML_L-'),
             sg.MLine(size=(20,100), key='-ML_M-')
            ]
        ], size = (1000, 100))

#移動用フレーム
frame_Move = sg.Frame('', 
        [
            [sg.Input(size=(20,100), key='-Input_I-'),
             sg.Input(size=(20,100), key='-Input_J-'),
             sg.Input(size=(20,100), key='-Input_K-'),
             sg.Input(size=(20,100), key='-Input_L-'),
             sg.Input(size=(20,100), key='-Input_M-'),
            ],
            [sg.Text('降下/上昇量(mm)を入力')]
        ], size = (1000, 100))

#ボタン用フレーム
frame_Button1 = sg.Frame('', 
        [
            [sg.Button('Slow\n2mm/min', key='-Slow-', size=(20,100), disabled=False),
             sg.Button('Fast\n10mm/min', key='-Fast-', size=(20,100), disabled=False),
             sg.Button('Set\nローカル座標を0に',  key='-Set-',  size=(20,100), disabled=False),
             sg.Button('Save',  key='-Save-',  size=(20,100), disabled=False),
             sg.Button('Save Stop',  key='-Savestop-',  size=(20,100), disabled=False)
            ]
        ], size = (1000, 100))

frame_Button2 = sg.Frame('', 
        [
             [sg.Button('Read\nファイル読み込み', key='-Read-', size=(20,100), disabled=False),
             sg.Button('Run',  key='-Run-',  size=(20,100), disabled=False),
             sg.Button('Stop', key='-Stop-', size=(20,100), disabled=False)
            ]
        ], size = (1000, 100))

#Preview用フレーム
frame_Preview = sg.Frame('', 
        [
            [sg.Text('Preview'),sg.MLine(size=(500,100), key='-ML_Preview-')],
        ], size = (1000, 200))

#Status用フレーム
frame_Status = sg.Frame('', 
        [
            [sg.Text('Status'), sg.MLine(size=(100,100), key='-ML_Status-')],
        ], size = (1000, 100))

layout = [
    [frame_Label],
    [frame_Disp],
    [frame_Move],
    [frame_Button1],
    [frame_Button2],
    [frame_Preview],
    [frame_Status]
]

window = sg.Window('MonitorControl', layout, resizable = True)

#ser = serial.Serial('COM6', 115200)

list_gcode = []
list_gcode_index = 0
is_running = False
is_saving = None
list_savefile = [['Time', 'Status', 'I', 'J', 'K', 'L', 'M']]
csv_header = ['Time', 'Status', 'I', 'J', 'K', 'L', 'M']

while True:
    event, values = window.read(timeout=10)

    ############################### EVENT ###############################
    # Read
    if event == '-Read-':
        # gcodeのファイル指定すること
        gcode = './MotorControl.txt'
        with open(gcode) as g:
            g_preview = g.read()
            window['-ML_Preview-'].update(g_preview)
        with open(gcode) as g:
            list_gcode = g.readlines()
            list_gcode_index = 0

    #Run  
    if event ==  '-Run-':
        is_running = True
    #インクリメント指令（Slow）
    if event == '-Slow-':
            g_slow =  'G91' + 'I' + values['-Input_I-'] + 'J' + values['-Input_J-'] + 'K' + values['-Input_K-'] + 'L' + values['-Input_L-'] + 'M' + values['-Input_M-'] + 'V2 W2 X2 Y2 Z2 \r\n'
            print(g_slow)
            ser.write(g_slow.encode('ascii'))
            ser.flush()
            window['-ML_Preview-'].update(g_slow)
    #インクリメント指令（Fast）   
    if event == '-Fast-':
            g_fast =   'G91' + 'I' + values['-Input_I-'] + 'J' + values['-Input_J-'] + 'K' + values['-Input_K-'] + 'L' + values['-Input_L-'] + 'M' + values['-Input_M-'] + 'V10 W10 X10 Y10 Z10 \r\n'
            ser.write(g_fast.encode('ascii'))
            ser.flush()
            window['-ML_Preview-'].update(g_fast)
    #ローカル座標設定
    if event == '-Set-':
            # g_set =  'G52' + 'I' + values['-Input_I-'] + 'J' + values['-Input_J-'] + 'K' + values['-Input_K-'] + 'L' + values['-Input_L-'] + 'M' + values['-Input_M-'] + '\r\n'
            g_set =  'G52 I0J0K0L0M0\r\n'
            ser.write(g_set.encode('ascii'))
            ser.flush()
            window['-ML_Preview-'].update(g_set)
    
    #SaveFile
    if event == '-Save-':
        is_saving = True
        with open('./Time&Disp.csv', 'a', newline="") as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerow(csv_header)
             
    if event == '-Savestop-':
        is_saving = False
             
             
            
    #ローカル座標設定
    if event == '-Set-':
        # g_set =  'G52' + 'I' + values['-Input_I-'] + 'J' + values['-Input_J-'] + 'K' + values['-Input_K-'] + 'L' + values['-Input_L-'] + 'M' + values['-Input_M-'] + '\r\n'
        g_set =  'G52 I0J0K0L0M0\r\n'
        ser.write(g_set.encode('ascii'))
        ser.flush()
        window['-ML_Preview-'].update(g_set)
           
    if event is None:
            print('exit')
            break
    
    ############################### GCODE ###############################
    ser_line = ""
    ser_json = None
    try:
        ser_line = ser.readline().decode('ascii')
        if "REPORT: " in ser_line:
            ser_json = json.loads(ser_line.replace("REPORT: ", ''))
    except:
        pass
    
    if ser_json is None:
        continue
    
    print(ser_json)
    #print(ser_json['Time'])
    window['-ML_I-'].update(ser_json['I'])
    window['-ML_J-'].update(ser_json['J'])
    window['-ML_K-'].update(ser_json['K'])
    window['-ML_L-'].update(ser_json['L'])
    window['-ML_M-'].update(ser_json['M'])
    window['-ML_Status-'].update(ser_json['Status'])

    #　Status：BUSY　でボタン無効化
    if ser_json['Status'] == 'BUSY':
        window['-Slow-'].update(disabled=True)
        window['-Fast-'].update(disabled=True)
        window['-Set-'].update(disabled=True)
        window['-Run-'].update(disabled=True)
        window['-Read-'].update(disabled=True)
        #window['-Stop-'].update(disabled=True)
        
    if ser_json['Status'] == 'IDLE' and is_running == False:
        window['-Slow-'].update(disabled=False)
        window['-Fast-'].update(disabled=False)
        window['-Set-'].update(disabled=False)
        window['-Run-'].update(disabled=False)
        window['-Read-'].update(disabled=False)
        #window['-Stop-'].update(disabled=False)

    if is_running:
        if ser_json['Status'] == 'IDLE':
            if list_gcode_index >= 0 and list_gcode_index < len(list_gcode):
            
                gc = list_gcode[list_gcode_index]
                print(gc)
                ser.write(gc.encode('ascii') + '\r\n'.encode('ascii')) 
                ser.flush()
                window['-ML_Preview-'].update(gc)
                list_gcode_index += 1
            else:
                window['-ML_Preview-'].update("Finish!!")
                list_gcode_index = -1
                list_gcode = []
                is_running = False
        if ser_json['Status'] == 'BUSY':
            pass                

    if is_saving is True:

        window['-Save-'].update(disabled=True)

        with open('./Time&Disp.csv', 'a', newline="") as f:
            writer = csv.writer(f, delimiter=",")
        # Time,Displacement
            writer.writerow([ser_json['Time'], ser_json['Status'], ser_json['I'], ser_json['J'], ser_json['K'], ser_json['L'], ser_json['M']])

    
    if is_saving is False:
        window['-Save-'].update(disabled=False)
        is_saving = None
        
window.close()


   
   

