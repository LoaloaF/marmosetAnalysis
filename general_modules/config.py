import logging 

LOGGING_LEVEL = logging.INFO
CONSOLE_LOGGING_FMT = f'%(levelname)s|%(name)s'
FILE_LOGGING_FMT = f'%(levelname)s|%(asctime)s|%(name)s'
LOGGING_FMT_MSG = f'\n\t%(message)s'
SPACER_LOGGING_FMT = f'%(message)s=====================================================\n'
LOG_TO_DIR = './logs'
LOG_TO_DIR = None

SENSOR_DATA_FNAME = "sensor_data.csv"
REWARD_DATA_FNAME = "reward.log"

PHTOTRES_SENSOR_ID = "photoResistor"
LICK_SENSOR_ID = "lickSensor"
DISTANCELEFT_SENSOR_ID = "distanceSensorLeft"

FRONT_CAM_FNAME = "camerafeed_0.mp4"
FRONT_CAM_TS_FNAME = "frameGrabber_0_stdout.txt"
SCENE_CAM_FNAME = "camerafeed_1.mp4"
SCENE_CAM_TS_FNAME = "frameGrabber_1_stdout.txt"
FACE_CAM_FNAME = "camerafeed_2.mp4"
FACE_CAM_TS_FNAME = "frameGrabber_2_stdout.txt"

EXPFRAME_TS_OUTFNAME = "expframe_ts"
LICK_OUTFNAME = "lick"
DIST_LEFT_OUTFNAME = "dist_left"
REWARD_OUTFNAME = "reward"
ONOFF_OUTFNAME = "onwoff_switches"
FRONTCAM_TS_OUTFNAME = "frontcam_ts"
SCENECAM_TS_OUTFNAME = "scenecam_ts"
FACECAM_TS_OUTFNAME = "facecam_ts"

FACECAM_VID_OUTFNAME = "facecam_annotated"
VIDEO_FILE_ENDING = ".avi"

#                 Y   X  WIDTH
FACE_CAM_CROP = (120,250,200)
FACE_CAM_FLIP = True

# LOG_OOD_DELTATIMES = False


"""
Feature requests:

have a preprocessing log at debug level written to a file that is part of the
preproc final dir



"""