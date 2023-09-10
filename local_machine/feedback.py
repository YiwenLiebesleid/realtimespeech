import threading
import tkinter as tk
import sound_recording
import numpy as np
import client_sb
from collections import defaultdict

NOT_SPEECH = "Not Speech"
current_correct_name = NOT_SPEECH
# load enrolled sample names
name_arr = []
name_radio_dic = dict()
# count the feedback times for every user
name_fb_cnt_dic = defaultdict(int)

# submit feedback audio to server, along with the feedback id
def save_feedback_audio_thread(correct_name_fb_id):
    recent_3_sec_np = np.concatenate(sound_recording.record_3_sec)
    client_sb.feedback_process("./feedback_collection/" + correct_name_fb_id, recent_3_sec_np)

# bind with submit button, display correct name, save recent 3 seconds' audio
def get_correct_name(v, feedback_lb):
    global name_radio_dic
    global name_fb_cnt_dic
    correct_name = name_radio_dic.get(v.get())
    feedback_lb.config(text=correct_name)
    name_fb_id = name_fb_cnt_dic[correct_name]
    name_fb_cnt_dic[correct_name] += 1

    # start a thread to submit to server
    threading.Thread(target=save_feedback_audio_thread
                     , args=(correct_name + "_" + str(name_fb_id),)).start()


# new frame: feedback from user to correct recognition
def feedback_page(main_frame):
    global name_arr
    global name_radio_dic
    name_arr = sound_recording.enrolled_names
    name_radio_dic = dict(zip([i for i in range(0, len(name_arr))], name_arr))

    feedback_left_frame = tk.Frame(main_frame)
    title_lb = tk.Label(feedback_left_frame, text = 'Correction', font=('Bold', 15))
    title_lb.pack(expand=True, anchor="center")
    feedback_lb = tk.Label(feedback_left_frame, text='result here', font=('Bold', 12))
    feedback_lb.pack(expand=True, anchor="center")

    # TRY: use radio button to select user
    v = tk.IntVar()
    for id,item in enumerate(name_arr):
        tk.Radiobutton(feedback_left_frame, text=item
                       , font=('8'), fg='#158aff'
                       , variable=v, value=id
                       # , indicatoron=False
                       ).pack(anchor='w', padx=60)

    feedback_left_frame.pack(side='left')


    # TRY: submit button
    feedback_right_frame = tk.Frame(main_frame)
    feedback_submit_btn = tk.Button(feedback_right_frame, text="Submit", font=(16),
                              fg='red', bd=1
                            , command=lambda:get_correct_name(v, feedback_lb))
    feedback_submit_btn.pack(expand=True, anchor="w", padx=40, ipadx=25, ipady=20)
    feedback_right_frame.pack(side='right')

    # disable button before recognition start
    # feedback_submit_btn["state"] = tk.DISABLED