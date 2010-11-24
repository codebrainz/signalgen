#!/usr/bin/env python
#
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

from optparse import OptionParser
from signalgen import SignalGen
import sys
import gst
import time
import warnings

# do this to hide a deprection warning on using the popen2 module in urwid
with warnings.catch_warnings():
    warnings.simplefilter('ignore', DeprecationWarning)
    from urwid import raw_display

def main():

    VOLUME_GRANULARITY = 0.01   # 0 - 1
    FREQ_GRANULARITY = 10       # 1 - 20000
    
    epilog = 'Written by Matthew Brush'
    desc = 'Values for wave are; sine=0, square=1, saw=2, triangle=3, \
silence=4, white_noise=4, pink_noise=6, sine_table=7, ticks=8.  You can adjust \
the waveform properties at runtime by using the following keys; up/down=volume, \
left/right=frequency, page up/page down=waveform.'
    
    parser = OptionParser(description=desc, epilog=epilog)
    
    parser.add_option('-f', '--freq', dest='freq', metavar='FREQ', 
        default='440', help='frequency of signal from 0-20000, default 440')
    parser.add_option('-v', '--volume', dest='volume', metavar='VOL',
        default='0.8', help='volume of signal from 0-1, default 0.8')
    parser.add_option('-w', '--wave', dest='wave', metavar='WAVE',
        default='0', help='oscillator waveform from 0-8, default 0')
    parser.add_option('-c', '--stdout', dest='stdout', action='store_true',
        default=False, help='outputs waveforms to stdout, default off')
    parser.add_option('-V', '--visualize', dest='visualize', 
        action='store_true', default=False, help='enable an X oscilloscope window, default off')
    parser.add_option('-a', '--audio', dest='audio', action='store_true',
        default=True, help='enable audio output, default on')
    parser.add_option('-q', '--quiet', dest='quiet', action='store_true',
        default=False, help="don't print to stdout or stderr, default off")
    
    opts, args = parser.parse_args()
    
    f = int(opts.freq)
    v = float(opts.volume)
    w = int(opts.wave)
    sout = bool(opts.stdout)
    vout = bool(opts.visualize)
    aout = bool(opts.audio)
    
    sg = SignalGen(f, v, w, aout, vout, sout)

    sg.start()
    playing = True
    last_vol = v

    s = raw_display.Screen()
    try:
        s.start()
        while True:
            try:
                ip = s.get_input()
                if 'q' in ip:
                    break
                elif 'up' in ip:
                    sg.ws.volume = sg.ws.volume + VOLUME_GRANULARITY
                elif 'down' in ip:
                    sg.ws.volume = sg.ws.volume - VOLUME_GRANULARITY
                elif 'left' in ip:
                    sg.ws.freq = sg.ws.freq - FREQ_GRANULARITY
                elif 'right' in ip:
                    sg.ws.freq = sg.ws.freq + FREQ_GRANULARITY
                elif 'page up' in ip:
                    sg.ws.waveform = sg.ws.waveform + 1
                elif 'page down' in ip:
                    sg.ws.waveform = sg.ws.waveform - 1
                elif 'm' in ip:
                    if playing:
                        last_vol = sg.ws.volume
                        sg.ws.volume = 0
                        playing = False
                    else:
                        sg.ws.volume = last_vol
                        playing = True
                
                if not opts.quiet:
                    line = 'waveform=%s, frequency=%s, volume=%s' % \
                        (sg.ws.waveform, sg.ws.freq, sg.ws.volume)
                    width, height = s.get_cols_rows()
                    blanks = width - len(line)
                    line = line + ' '*blanks + '\r'
                    if opts.stdout:
                        sys.stderr.write(line)
                        sys.stderr.flush()
                    else:
                        sys.stdout.write(line)
                        sys.stdout.flush()

            except KeyboardInterrupt: 
                break
    finally:
        s.stop()
    
    return
    

if __name__ == '__main__': main()
