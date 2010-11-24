# signalgen.py
# 
# Copyright 2009 Matthew Brush <mbrush AT leftclick DOT ca>
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.
import gst
from wavesource import WaveSource

class SignalGen(object):
    
    def __init__(self, freq=440, volume=0.8, wave=0, audio=True, 
        visualize=False, stdout=False):
            
        if not audio and not visualize and not stdout:
            raise Exception('at least one sink/output must be enabled')
    
        # create pipeline
        self.pipeline = gst.Pipeline('signalgen')
        
        # create audiotestsrc
        self.ws = WaveSource(freq, volume, wave)
        
        # create tee to split off to three sinks
        self.tee = gst.element_factory_make('tee', 'tee')
    
        self.aconv = gst.element_factory_make('audioconvert', 'aconv')
        
        self.pipeline.add(self.ws.element, self.aconv, self.tee)

        # link the source into the tee
        gst.element_link_many(self.ws.element, self.aconv, self.tee)
        
        if visualize:
        
            # create visualizer elements
            self.vqueue = gst.element_factory_make('queue', 'vqueue')
            self.mscope = gst.element_factory_make('monoscope', 'mscope')
            self.color = gst.element_factory_make('ffmpegcolorspace', 'color')
            self.xsink = gst.element_factory_make('xvimagesink', 'xsink')
            
            self.pipeline.add(self.vqueue, self.mscope, self.color, self.xsink)
                
            gst.element_link_many(self.vqueue, self.mscope, self.color, self.xsink)
                
            self.tee.link(self.vqueue)
        
        if stdout:
        
            # create stdout elements
            self.squeue = gst.element_factory_make('queue', 'squeue')
            self.fsink = gst.element_factory_make('fdsink', 'fsink')
            self.fsink.set_property('fd', 1)
            
            self.pipeline.add(self.squeue, self.fdsink)
            
            self.squeue.link(self.fsink)
            
            self.tee.link(self.squeue)
        
        if audio:
            
            # create audio out elements
            self.aqueue = gst.element_factory_make('queue', 'aqueue')
            self.asink = gst.element_factory_make('autoaudiosink', 'asink')
            
            #self.pipeline.add(self.asink)
            self.pipeline.add(self.aqueue, self.asink)
            
            self.aqueue.link(self.asink)
            
            self.tee.link(self.aqueue)
            #self.tee.link(self.asink)

        #self.pipeline.set_state(gst.STATE_PLAYING)
    def play(self):
        self.start()
    
    def start(self):
        self.pipeline.set_state(gst.STATE_PLAYING)
    
    def pause(self):
        self.pipeline.set_state(gst.STATE_PAUSED)
