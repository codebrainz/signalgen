#!/usr/bin/env python2
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

#TODO: - close down pipeline and exit when video window is closed, or at least
#        don't stop audio when it's closed.

import sys
from optparse import OptionParser
from urwid import raw_display
from waveforms import WAVEFORMS

# moved to main() function, see note
#from signalgen import SignalGen

VOLUME_GRANULARITY  = 0.01      # 0 - 1
FREQ_GRANULARITY    = 10        # 1 - 20000

def parse_arguments():

    desc = """Values for wave must be one of: %s.  You can adjust the waveform 
properties at runtime by using the following keys; up/down=volume, 
left/right=frequency, page up/page down=waveform.""" % ", ".join(WAVEFORMS)

    parser = OptionParser(description=desc, epilog="Written by Matthew Brush.")
    
    parser.add_option('-f', '--freq', dest='freq', metavar='FREQ', 
        action="store", type="int", default=440, 
        help='frequency of signal from 0-20000, default 440')
        
    parser.add_option('-v', '--volume', dest='volume', metavar='VOL',
        action="store", type="float", default=0.8, 
        help='volume of signal from 0-1, default 0.8')
        
    parser.add_option('-w', '--wave', dest='wave', metavar='WAVE',
        action="store", default="sine", choices=tuple(WAVEFORMS),
        help="oscillator waveform name, default 'sine'")
        
    parser.add_option('-c', '--stdout', dest='stdout', action='store_true',
        default=False, help='outputs waveforms to stdout, default off')
        
    parser.add_option('-V', '--visualize', dest='visualize', 
        action='store_true', default=False, 
        help='enable an X oscilloscope window, default off')
        
    parser.add_option('-a', '--audio', dest='audio', action='store_true',
        default=True, help='enable audio output, default on')
    
    parser.add_option('-q', '--quiet', dest='quiet', action='store_true',
        default=False, help="don't print to stdout or stderr, default off")
    
    opts, args = parser.parse_args()
    
    return (opts.freq, opts.volume, opts.wave, opts.stdout, opts.visualize, 
                opts.audio, opts.quiet)


def main():

    freq, vol, wave, stdout_, visout, audout, quiet = parse_arguments()
    
    # imported here to avoid gstreamer hijacking command-line arguments.
    from wavegen import WaveGen, EosException 
    
    sg = WaveGen(freq, vol, wave, audout, visout, stdout_, quiet)

    sg.start()
    playing = True
    last_vol = vol

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
                    sg.ws.next_waveform()
                elif 'page down' in ip:
                    sg.ws.previous_waveform()
                elif 'm' in ip:
                    if playing:
                        last_vol = sg.ws.volume
                        sg.ws.volume = 0
                        playing = False
                    else:
                        sg.ws.volume = last_vol
                        playing = True
                
                if not quiet:
                    line = 'waveform=%s, frequency=%s, volume=%s' % \
                        (sg.ws.waveform, sg.ws.freq, sg.ws.volume)
                    width, height = s.get_cols_rows()
                    blanks = width - len(line)
                    line = line + ' '*blanks + '\r'
                    if stdout_:
                        sys.stderr.write(line)
                        sys.stderr.flush()
                    else:
                        sys.stdout.write(line)
                        sys.stdout.flush()

            except KeyboardInterrupt: 
                break
            except EosException:
                break
    finally:
        s.stop()
    
    return
    

if __name__ == '__main__': main()
