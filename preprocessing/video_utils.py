import cv2
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from general_modules.config import *

def check_video_file(video_file, logger):
    vid_cap = open_video(video_file, logger)
    release_cap(vid_cap)
    return vid_cap is not None
    
def open_video(video_file, logger):
    # Open the video file using OpenCV and return the video capture object.
    vid_cap = cv2.VideoCapture(video_file)
    if not vid_cap.isOpened():
        logger.error(f"Could not open the video file: {video_file}")
        return
    return vid_cap

def get_frame_count(vid_cap):
    return int(vid_cap.get(cv2.CAP_PROP_FRAME_COUNT))

def get_frame_deltatime(vid_cap):
    return pd.Timedelta(seconds=1/vid_cap.get(cv2.CAP_PROP_FPS))

# def extract_mp4_frames(vid_cap, index_collections):
#     if vid_cap is None:
#         return
#     frame_count = get_frame_count(vid_cap)

#     frames = []
#     for frame_number in range(frame_count):
#         ret, frame = cap.read()
#         if not ret:
#             break
        
#         frames = [frame for index_collection in index_collections 
#                   if frame_number in index_collection]
#     return frames

def release_cap(vid_cap):
    if vid_cap is not None:
        vid_cap.release()

def write_text(frame, text, xy, color=(255,255,255), font_scale=.8, 
               font_thickness=2):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.putText(frame, text, xy, font, font_scale, color, font_thickness)

def write_facecam_vid(vid_fname, frame_ts, lick_frames, reward_frames, 
                      dest_path, output_fname, logger):
    vid_cap = open_video(vid_fname, logger)
    if frame_ts is None or vid_cap is None:
        logger.error("No annotated facecam video will be written.")
        return
    logger.info("Writing annotated facecamera video")

    fourcc = cv2.VideoWriter_fourcc(*'H264')
    x, y, width = FACE_CAM_CROP
    fps = vid_cap.get(cv2.CAP_PROP_FPS)
    dest_fname = os.path.join(dest_path, output_fname+VIDEO_FILE_ENDING)
    out = cv2.VideoWriter(dest_fname, fourcc, fps, (width, width))

    last_reward_frame = -1
    for i, ts in frame_ts.iterrows():
        ret, frame = vid_cap.read()
        if not ret:
            break  

        frame = frame[x:x+width,y:y+width]
        frame = cv2.flip(frame, 0)

        write_text(frame, ts.start.strftime('%H:%M:%S'), (120, 20), 
                   font_scale=.5, font_thickness=1)
        if lick_frames.iloc[i]:
            write_text(frame, "Lick", (10, width-13))
        if any(reward_frames.iloc[i:i+10]):
            write_text(frame, "Reward", (50, width-13), color=(0,255,0))

        out.write(frame)

    out.release()
    release_cap(vid_cap)