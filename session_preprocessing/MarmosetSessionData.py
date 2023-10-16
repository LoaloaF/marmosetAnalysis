import os
import pandas as pd
import numpy as np

from config import *
from CustomLogger import CustomLogger

from data_utils import unix2pd_datetime
from data_utils import check_timeseries_integrity
from video_utils import write_facecam_vid

from data_io import read_metadata_file
from data_io import read_sensor_file
from data_io import read_reward_file
from data_io import read_video_ts_files
from data_io import write_dict2json
from data_io import write_hdf5
from data_io import load_prepoc_data

class MarmosetSessionData():
    logger = CustomLogger(__name__, write_to_directory=LOG_TO_DIR)

    def __init__(self, data_path, readwrite_preproc="write"):
        # load the metadata
        self.metad = read_metadata_file(data_path)
        
        # read the session name from the datapath to setup the logger headers
        _name = "{session_start_date}_{session_start_time}".format(**self.metad)
        self.logger.extend_fmt(f'|{_name}')

        if readwrite_preproc == "write":
            # load the sensor data and preprocess it
            sensor_data = read_sensor_file(data_path, self.logger)
            photores_d, lick_d, dist_left_d = self._extract_sensors(sensor_data)
            self.expframe_ts_data = self._preproc_photores_data(photores_d)
            self.lick_data = self._preproc_lick_data(lick_d)
            self.dist_left_data = self._preproc_dist_data(dist_left_d)

            # load the reward data
            self.reward_data = read_reward_file(data_path, self.logger)
            
            # load the video frame timestamps data and preprocess, check videos
            frontcam_ts, scenecam_ts, facecam_ts = read_video_ts_files(data_path, 
                                                                    self.logger)
            ret = self._preproc_expframe_ts_data(frontcam_ts, scenecam_ts, facecam_ts)
            self.frontcam_ts, self.scenecam_ts, self.facecam_ts = ret
            
            # prepare saving the data, create an annotated face camera video
            dest_path = os.path.join(data_path, "preproc_"+self.session_name)
            self._save_prepoc_data(dest_path)
            write_facecam_vid(vid_fname=os.path.join(data_path, FACE_CAM_FNAME),
                              frame_ts=self.frontcam_ts,
                              lick_frames=self._get_lickframes(self.facecam_ts),
                              reward_frames=self._get_rewardframes(self.facecam_ts),
                              dest_path=dest_path,
                              output_fname=FACECAM_VID_OUTFNAME,
                              logger=self.logger)
        
        elif readwrite_preproc == 'read':
            (self.expframe_ts_data, self.lick_data, self.dist_left_data, 
            self.reward_data, self.frontcam_ts, self.scenecam_ts, 
            self.facecam_ts) = load_prepoc_data(data_path, self.logger)

        else:
            self.logger.critical((f"Invalid input for `readwrite_preproc`: "
                                 f"{readwrite_preproc}. Valid inputs are `read`"
                                 f" and `write`"))
            exit(1)
        self.logger.spacer()

    def _extract_sensors(self, sensor_data):
        def process_single_sensor(sensor_id):
            sensor_dat = sensor_data[sensor_data.id == sensor_id]
            sensor_dat = sensor_dat.set_index('logging_timestamp')
            sensor_dat = sensor_dat.drop("id", axis=1)
            sensor_dat = sensor_dat.squeeze().rename(sensor_id)#.sort_index()
            return sensor_dat
        return [process_single_sensor(s_id) for s_id 
                in (PHTOTRES_SENSOR_ID,LICK_SENSOR_ID,DISTANCELEFT_SENSOR_ID)]
        
    def _preproc_photores_data(self, photores_data):
        if photores_data is None:
            return
        self.logger.info("Processing photoresistor data")
        
        # to be implmented: calculate frame render times
        return photores_data

    def _preproc_lick_data(self, lick_data):
        if lick_data is None:
            return
        self.logger.info("Processing lick sensor data")

        lick_data.iloc[-1] = 0
        lick_onoff = lick_data.diff().fillna(0).astype(int)

        lick_d = {}
        lick_d['start'] = lick_data.iloc[np.where(lick_onoff==1)].index
        lick_d['end'] = lick_data.iloc[np.where(lick_onoff==-1)[0] -1].index
        lick_data = pd.DataFrame(lick_d)
        lick_data['duration'] = lick_d['end']-lick_d['start']
        return lick_data

    def _preproc_dist_data(self, dist_left_data):
        if dist_left_data is None:
            return
        self.logger.info("Processing distance sensor data")

        check_timeseries_integrity(dist_left_data, self.logger)
        windowsize = self.metad["dist_sensor_mean_windowsize"]
        dist_left_data = dist_left_data.rolling(windowsize).mean()
        return dist_left_data

    def _preproc_expframe_ts_data(self, frontcam_ts, scenecam_ts, facecam_ts):
        ts_data = []
        for ts in (frontcam_ts, scenecam_ts, facecam_ts):
            if ts is None:
                ts_data.append(None)
                continue
            
            frame_data = {"start":ts}
            frame_ts_end = np.roll(frame_data["start"].values, -1)
            frame_deltat = pd.Timedelta(seconds=1/self.metad["cameraFPS"])
            frame_ts_end[-1] = frame_ts_end[-2] + frame_deltat
            frame_data["end"] = frame_ts_end
            
            frame_data = pd.DataFrame(frame_data)
            frame_data['duration'] = frame_data['end']-frame_data['start']
            ts_data.append(frame_data)
        return ts_data
    
    def _get_lickframes(self, which_cam_ts):
        if which_cam_ts is not None and self.lick_data is not None:
            def check_lick(frame_d):
                within_startlick = ((frame_d.start <self.lick_data.start) &
                                (frame_d.end >self.lick_data.start))
                within_endlick = ((frame_d.start <self.lick_data.end) &
                                (frame_d.end >self.lick_data.end))
                within_longlick = ((frame_d.start >self.lick_data.start) &
                                (frame_d.end <self.lick_data.end))
                return any(within_startlick | within_endlick | within_longlick)
            return which_cam_ts.apply(check_lick, axis=1)
    
    def _get_rewardframes(self, which_cam_ts):
        if which_cam_ts is not None and self.lick_data is not None:
            check_rew = lambda fr_d: any((self.reward_data.index>fr_d.start) & 
                                         (self.reward_data.index<fr_d.end))
            return which_cam_ts.apply(check_rew, axis=1)

    def _save_prepoc_data(self, dest_path):
        os.makedirs(dest_path, exist_ok=True)
        fname_mapping = {EXPFRAME_TS_OUTFNAME: self.expframe_ts_data,
                         LICK_OUTFNAME: self.lick_data,
                         DIST_LEFT_OUTFNAME: self.dist_left_data,
                         REWARD_OUTFNAME: self.reward_data,
                         FRONTCAM_TS_OUTFNAME: self.frontcam_ts,
                         SCENECAM_TS_OUTFNAME: self.scenecam_ts,
                         FACECAM_TS_OUTFNAME: self.facecam_ts}
        [write_hdf5(dest_path, fname, data, self.logger) 
         for fname, data in fname_mapping.items()]
        write_dict2json(self.metad, dest_path, "metadata.json")

    def __str__(self):
        msg = f"{self.session_length}"
        return msg

    @property
    def session_name(self):
        start_str = self.session_start.strftime("%Y-%m-%d_%H-%M-%S")
        duration_h_str = int(self.session_length.total_seconds() //3600)
        duration_min_str = int((self.session_length.total_seconds() %3600)//60)
        return f"{start_str}_{duration_h_str}h-{duration_min_str}min"

    @property
    def session_start(self):
        return self.expframe_ts_data.index[0]
    
    @property
    def session_start_date(self):
        return self.session_start.date()
    
    @property
    def session_start_time(self):
        return self.session_start.time()
    
    @property
    def session_stop(self):
        return self.expframe_ts_data.index[-1]
    
    @property
    def session_length(self):
        return self.session_stop-self.session_start 
    
    @property
    def reward_delivered_ml(self):
        return self.reward_data.shape[0] *self.metad['rewardVolume'] /1000
    
    @property
    def cum_reward_delivered_ml(self):
        return np.cumsum(self.reward_data *self.metad['rewardVolume'] /1000)
    
    @property
    def n_reward_events(self):
        return self.reward_data.shape[0]
    
    @property
    def reward_events_per_hour(self):
        return self.n_reward_events /(self.session_length.total_seconds()/3600)