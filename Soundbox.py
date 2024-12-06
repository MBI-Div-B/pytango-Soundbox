#!/home/labuser/micromamba/envs/sardana/bin/python
# -*- coding: utf-8 -*-


# Copyright (C) 2020  MBI-Division-B
# MIT License, refer to LICENSE file
# Author: Martin Hennecke / Email: hennecke@mbi-berlin.de

from tango.server import run, Device
from tango.server import attribute, command
from tango import DevState, AttrWriteType

from pydub import AudioSegment
from pydub.playback import play

from multiprocessing import Process
import time

class Soundbox(Device):
    sound = attribute(
        label="Sound",
        dtype="str",
        access=AttrWriteType.READ_WRITE,
    )

    def init_device(self):
        Device.init_device(self)
        self.__sound = ''
        self.set_state(DevState.ON)

    def delete_device(self):
        pass

    def read_sound(self):
        return self.__sound

    def write_sound(self, value):
        self.__sound = value
        sound = AudioSegment.silent(duration=500)+AudioSegment.from_file(value)+AudioSegment.silent(duration=500)

        process = Process(target=play, args=(sound,))
        process.start()
        #play(AudioSegment.silent(duration=500)+sound+AudioSegment.silent(duration=500))

# start the server
if __name__ == "__main__":
    Soundbox.run_server()