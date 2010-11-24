# audiogen.py
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

class WaveSource(object):
    
    _audiotestsrc = None

#-------------------------------------------------------------------------------
# constants
    class Waveforms:
        """available waveforms"""
        SINE = 0
        SQUARE = 1
        SAW = 2
        TRIANGLE = 3
        SILENCE = 4
        WHITE_NOISE = 5
        PINK_NOISE = 6
        SINE_TABLE = 7
        TICKS = 8
    
#-------------------------------------------------------------------------------
# frequency    
    _freq = 5000
    def _get_freq(self): return self._freq
    def _set_freq(self, value):
        if value < 0: value = 0
        if value > 20000: value = 20000
        self._freq = value
        self._audiotestsrc.set_property('freq', self._freq)
    freq = property(_get_freq, _set_freq, 'change the waveform frequency')
    
#-------------------------------------------------------------------------------
# volume
    _vol = 0.1
    def _get_vol(self): return self._vol
    def _set_vol(self, value):
        if value < 0: value = 0
        if value > 1: value = 1
        self._vol = value
        self._audiotestsrc.set_property('volume', self._vol)
    volume = property(_get_vol, _set_vol, 'change the waveform amplitude/volume')

#-------------------------------------------------------------------------------
# gstreamer element getter
    @property
    def element(self): return self._audiotestsrc

#-------------------------------------------------------------------------------
# waveform
    _wave = 0
    def _get_wave(self): return self._wave
    def _set_wave(self, value):
        if value > 8: value = 8
        if value < 0: value = 0
        self._wave = value
        self._audiotestsrc.set_property('wave', self._wave)
    waveform = property(_get_wave, _set_wave, 'change the waveform type')
    
    
    def __init__(self, freq=500, volume=0.1, wave=0):
        
        self._audiotestsrc = gst.element_factory_make('audiotestsrc', 'audio')
        
        self.freq = freq
        self.volume = volume
        self.waveform = wave

    def __str__(self):
        s = ('audiotestsrc freq=%s volume=%s wave=%s' % 
            (self.freq, self.volume, self.waveform))
        return s
