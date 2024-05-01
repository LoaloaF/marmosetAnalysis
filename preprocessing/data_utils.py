import os
import json
import pandas as pd
import numpy as np
from datetime import timedelta as datetime_timedelta

from .video_utils import open_video
from .video_utils import get_frame_count
from .video_utils import release_cap

def unix2pd_datetime(tstamps, unit="s"):
    datetimes = pd.to_datetime(tstamps, unit=unit, origin='unix', errors='coerce')
    return datetimes

def pdTimetelta2datetimeTimedelta(pd_deltatime):
    days = pd_deltatime.days
    seconds = pd_deltatime.seconds
    mseconds = pd_deltatime.microseconds
    return datetime_timedelta(days=days, seconds=seconds, microseconds=mseconds)

def check_negative_deltatimes(times, logger):
    deltatimes = np.insert(np.diff(times), 0, np.nan)
    neg_deltatimes_mask = deltatimes<0
    
    if neg_deltatimes_mask.any():
        n_negs = sum(neg_deltatimes_mask)
        logger.warning([f"{n_negs} negative timedeltas detected [s]",
                        "These values will be removed:",
                        str(deltatimes[neg_deltatimes_mask])])
    return neg_deltatimes_mask

def check_timeseries_integrity(times, logger):
    deltatimes = times.index.to_series().diff().dt.total_seconds() *1e3
    med, std = np.nanmedian(deltatimes), np.nanstd(deltatimes)
    within_delta = lambda d, delta: (d<med+(delta)) & (d>max(med-delta, 0))
    
    one_ms = within_delta(deltatimes, 1)
    one_stds = within_delta(deltatimes, std*1)
    two_stds = within_delta(deltatimes, std*2)
    three_stds = within_delta(deltatimes, std*3)
    ood = ~three_stds

    msg = []
    msg.append(f"Median: {med:.3f}, STD: {std:.3f}")
    msg.append((f"Within 1 ms ({max(med-1,0):.3f} ms - {med+1:.3f} ms):"
                f" {one_ms.sum()*100/len(times):.1f}%"))
    msg.append((f"Within 1 STD ({max(med-1*std,0):.3f} ms - {med+1*std:.3f} ms):"
                f" {one_stds.sum()*100/len(times):.1f}%"))
    msg.append((f"Within 2 STD ({max(med-2*std,0):.3f} ms - {med+2*std:.3f} ms):"
                f" {two_stds.sum()*100/len(times):.1f}%"))
    msg.append((f"Within 3 STD ({max(med-3*std,0):.3f} ms - {med+3*std:.3f} ms):"
                f" {three_stds.sum()*100/len(times):.1f}%"))
    msg.append(f"Out of distribution deltatimes: {ood.sum()}")
    # if config.LOG_OOD_DELTATIMES:
    #     msg.append(f"Out of distribution deltatimes:\n{deltatimes[ood]}")
    logger.info(msg)

def check_video_ts_match(frame_tstamps, vid_fname, logger):
    vid_cap = open_video(vid_fname, logger)
    vid_nframes = get_frame_count(vid_cap)
    n_frame_ts = frame_tstamps.shape[0]
    if vid_nframes != n_frame_ts:
        logger.warning(f"{vid_fname}:\nVideo has {vid_nframes} frames"
                       f", but timestamp file has {n_frame_ts} entries.\n"
                       f"Processing will assume matching 0-indices.")
    release_cap(vid_cap)