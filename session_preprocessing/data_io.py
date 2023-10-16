import os
import json
import numpy as np
import pandas as pd

from config import *
from data_utils import check_negative_deltatimes
from data_utils import check_video_ts_match
from data_utils import unix2pd_datetime

from video_utils import check_video_file

def read_metadata_file(data_path):
    try:
        return read_json(data_path, "metadata.json")
    except FileNotFoundError as e:
        start_date, start_time = data_path.split(os.path.sep)[-2:]
        return {"rewardVolume":40, "interRewardInterval":3, "distanceLimit":6,
                "cameraFPS":30, "session_start_date": start_date,
                "session_start_time": start_time,
                "dist_sensor_mean_windowsize": 10,
                "notes": read_notes_txt_file(data_path, "notes.txt")}

def read_sensor_file(data_path, logger):
    logger.info(f"Loading sensor data")

    try:
        # Read the sensor data CSV file
        sen_filename = os.path.join(data_path, SENSOR_DATA_FNAME)
        sensor_d = pd.read_csv(sen_filename).iloc[:-1]
        sensor_d.drop(["arduino_timestamp", "computer_timestamp"], axis=1, 
                            inplace=True)
        
        mask = check_negative_deltatimes(sensor_d.logging_timestamp, logger)
        sensor_d = sensor_d[~mask]
        sensor_d.logging_timestamp = unix2pd_datetime(sensor_d.logging_timestamp)
        return sensor_d

    except FileNotFoundError as e:
        logger.error(f"\{e} Sensor data will be None.")
        return None

def read_reward_file(data_path, logger):
    logger.info(f"Loading and processing reward data")

    try:
        reward_d_fname = os.path.join(data_path, REWARD_DATA_FNAME)
        with open(reward_d_fname, 'r') as rew_file:
            tstamps = []
            for line in rew_file:
                try:
                    tstamps.append(float(line.split(" ")[-1]) )
                except ValueError as e:
                    logger.warning(f"{e} -> Line will be skipped")
        return pd.Series(True, unix2pd_datetime(tstamps), name='reward_events')

    except FileNotFoundError as e:
        logger.error(f"{e} - Reward events data will be None.")
        return None
    
def read_video_ts_files(data_path, logger):
    logger.info(f"Loading and processing video, vid-timestamp data")

    frame_tstamps = []
    ts_fnames = (FRONT_CAM_TS_FNAME, SCENE_CAM_TS_FNAME, 
                    FACE_CAM_TS_FNAME)
    vid_fnames = (FRONT_CAM_FNAME, SCENE_CAM_FNAME, 
                    FACE_CAM_FNAME)
    for i in range(len(ts_fnames)):
        try:
            video_ts_file = os.path.join(data_path, ts_fnames[i])
            frame_ts = pd.read_csv(video_ts_file, sep=" ", header=None).iloc[:,1]
            frame_ts = pd.Index(unix2pd_datetime(frame_ts).values)

            vid_fname = os.path.join(data_path, vid_fnames[i])
            video_ok = check_video_file(vid_fname, logger)
            if not video_ok:
                logger.error(f"Frame timestamps data will be None.")
                frame_tstamps.append(None)
                continue
            
            check_video_ts_match(frame_ts, vid_fname, logger)
            frame_tstamps.append(frame_ts)

        except FileNotFoundError as e:
            logger.error(f"{e} Frame timestamps data will be None.")
            frame_tstamps.append(None)
    return frame_tstamps

def read_json(data_path, fname):
    full_fname = os.path.join(data_path, fname)

    with open(full_fname, 'r') as json_file:
        data = json.load(json_file)
    return data

def write_dict2json(dic, dest_path, output_fname):
    dest_fname = os.path.join(dest_path, output_fname)
    with open(dest_fname, 'w') as json_file:
        json.dump(dic, json_file, indent=4)

def read_notes_txt_file(data_path, fname):
    full_fname = os.path.join(data_path, fname)
    try:
        with open(full_fname, "r") as file:
            notes = file.read()
    except FileNotFoundError:
        return ""
        
def write_hdf5(dest_path, output_fname, data, logger):
    if data is not None:
        dest_fname = os.path.join(dest_path, output_fname+".hdf5")
        data.to_hdf(dest_fname, key='data', format='table', complib='zlib', 
                    complevel=1, mode='w')
    else:
        logger.warning(f"{output_fname} is None. No file will be written.")

def read_hdf5(data_path, fname, logger):
    try:
        full_fname = os.path.join(data_path, fname+".hdf5")
        return pd.read_hdf(full_fname, key='data')
    except FileNotFoundError as e:
        logger.error(f"{output_fname} not found. Data will be None.")
        return None

def load_prepoc_data(data_path, logger):
    fnames = (EXPFRAME_TS_OUTFNAME, LICK_OUTFNAME, DIST_LEFT_OUTFNAME, 
              REWARD_OUTFNAME, FRONTCAM_TS_OUTFNAME, SCENECAM_TS_OUTFNAME, 
              FACECAM_TS_OUTFNAME)
    return [read_hdf5(data_path, fn, logger) for fn in fnames]