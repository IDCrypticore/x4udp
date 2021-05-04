#!/usr/bin/env python

import signal
import sys
import time
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

# Signal handler for stopping pipeline before destruction, so that Argus keeps ok.
def signal_handler(sig, frame):
    p.set_state(Gst.State.NULL)
    sys.exit(0)

# Initialize gstreamer
GObject.threads_init()
Gst.init(None)

# Define pipeline 
#gst_str = "nvarguscamerasrc ! video/x-raw(memory:NVMM),format=(string)NV12,width=(int)640,height=(int)480, framerate=30/1 ! nvvidconv ! xvimagesink "
gst_str = "udpsrc port=5000 ! application/x-rtp,encoding-name=H264 ! rtpjitterbuffer latency=1000 drop-on-latency=false ! rtph264depay ! h264parse ! nvv4l2decoder ! nvvidconv ! xvimagesink"

# Create the pipeline
p = Gst.parse_launch (gst_str)

# Register signal handler for proper termination if receiving SIGINT such as Ctrl-C
signal.signal(signal.SIGINT, signal_handler)

# Start the pipeline
p.set_state(Gst.State.READY)
p.set_state(Gst.State.PAUSED)
p.set_state(Gst.State.PLAYING)

# Run for 10s 
time.sleep(10)

# Done. Stop the pipeline before clean up on exit.
p.set_state(Gst.State.NULL)
exit(0)
