'''
Code by Charlie Buren
Based off code that can be found here: https://github.com/prophesee-ai/event-based-get-started/blob/main/metavision_time_surface/metavision_time_surface.py
'''

from metavision_core.event_io import EventsIterator, LiveReplayEventsIterator, is_live_camera
from metavision_sdk_core import EventPreprocessor, MostRecentTimestampBuffer
from metavision_sdk_ui import EventLoop, BaseWindow, MTWindow, UIAction, UIKeyEvent
import numpy as np
import cv2
import argparse

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Metavision Time Surface sample.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-i', '--input-event-file', dest='event_file_path', default="",
        help="Path to input event file (RAW or HDF5). If not specified, the camera live stream is used. "
        "If it's a camera serial number, it will try to open that camera instead.")
    args = parser.parse_args()
    return args


def main():
    """ Main """
    args = parse_args()

    last_processed_timestamp = 0

    # Events iterator on Camera or event file
    mv_iterator = EventsIterator(input_path=args.event_file_path, delta_t=10000)
    height, width = mv_iterator.get_size()  # Camera Geometry

    # Helper iterator to emulate realtime
    if not is_live_camera(args.event_file_path):
        mv_iterator = LiveReplayEventsIterator(mv_iterator)

    # Window - Graphical User Interface
    with MTWindow(title="Metavision Events Viewer", width=width, height=height,
                  mode=BaseWindow.RenderMode.BGR) as window:
        def keyboard_cb(key, scancode, action, mods):
            if key == UIKeyEvent.KEY_ESCAPE or key == UIKeyEvent.KEY_Q:
                window.set_close_flag()

        window.set_keyboard_callback(keyboard_cb)

        time_surface = MostRecentTimestampBuffer(rows=height, cols=width, channels=1)
        ts_prod = EventPreprocessor.create_TimeSurfaceProcessor(input_event_width=width, input_event_height=height, split_polarity=False)

        img = np.empty((height, width), dtype=np.uint8)

        # Process events
        for evs in mv_iterator:
            # Dispatch system events to the window
            EventLoop.poll_and_dispatch()
            if len(evs) == 0:
                continue
            ts_prod.process_events(cur_frame_start_ts=evs[0][3], events_np=evs, frame_tensor_np=time_surface.numpy())
            last_processed_timestamp = evs[-1][3]
            time_surface.generate_img_time_surface(last_processed_timestamp, 10000, img)
            window.show_async(cv2.applyColorMap(img, cv2.COLORMAP_JET))

            if window.should_close():
                break


if __name__ == "__main__":
    main()