import pygame
import math
import pedalboard
import sounddevice as sd
from pedalboard.io import AudioFile, AudioStream

from pedalboard import Pedalboard, Chorus, Distortion, Reverb

def pedalboardtests():
    # Create an empty Pedalboard object:
    my_pedalboard = Pedalboard()

    # Treat this object like a Python list:
    my_pedalboard.append(Chorus())
    my_pedalboard.append(pedalboard.Phaser())
    #my_pedalboard.append(Distortion())
    my_pedalboard.append(Reverb())
    my_pedalboard.append(pedalboard.Bitcrush(4))

    # Pass audio through this pedalboard:

    with AudioFile("/Users/admin/Documents/GitHub/SillyGame/scripts/test.mp3") as f:
        print(f.duration) # => 30.0
        samplerate = f.samplerate
        print(f.num_channels)
        output_audio = my_pedalboard(f.read(f.samplerate * 100), samplerate)

    with AudioFile("test2.mp3", "w", samplerate=44100, num_channels=2) as f:
       f.write(output_audio)

def audio_stream():
    output_device_name = AudioStream.output_device_names[0]
    input_device_name = AudioStream.input_device_names[0]
    stream = AudioStream(input_device_name, output_device_name)
    stream.plugins.append(pedalboard.Gain(12))
    stream.run()  # Run the stream until Ctrl-C is received

class Realtime_Audio():
    
    def __init__(self):
        self.timesegment = 1 / 60
        self.my_pedalboard = Pedalboard()
        self.segment = 0

        # Treat this object like a Python list:
        #self.my_pedalboard.append(Chorus())
        #self.my_pedalboard.append(pedalboard.Phaser())
        #my_pedalboard.append(Distortion())
        #self.my_pedalboard.append(Reverb())
        #self.my_pedalboard.append(pedalboard.VST3Plugin("/Library/Audio/Plug-Ins/VST3/Cymatics Origin.vst3"))
        #self.my_pedalboard.append(pedalboard.Bitcrush(4))
        
    
    def update(self):
        with AudioFile("/Users/admin/Documents/GitHub/SillyGame/scripts/test.mp3") as f:
            samplerate = f.samplerate
            self.segment += samplerate * self.timesegment
            output_audio = self.my_pedalboard(f.read(self.segment), samplerate)
            print(output_audio)
            output_audio *= 0.1
            
        
        #with AudioFile("test2.mp3", "w", samplerate=44100, num_channels=2) as f:
        #    f.write(output_audio)
        
        h = pygame.mixer.Sound(output_audio)
        channel = pygame.mixer.Channel(0)
        h.set_volume(0.1)
        channel.play(h)
    
    def processor(self):
        pass
    
    def playback(self):
        pass
    
    def add_effect(self):
        pass
class MusicManager():
    
    def __init__(self, game):
        self.game = game
        self.sfx = {
            'jump': pygame.mixer.Sound('data/sfx/jump.wav'),
            'dash': pygame.mixer.Sound('data/sfx/dash.wav'),
            'hit': pygame.mixer.Sound('data/sfx/hit.wav'),
            'shoot': pygame.mixer.Sound('data/sfx/shoot.wav'),
            'spring': pygame.mixer.Sound('data/sfx/spring.wav'),
            'ambience': pygame.mixer.Sound('data/sfx/ambience.wav'),
        }
        
        self.music = {
            'base' : pygame.mixer.Sound('data/music.wav'),
            'base2' : pygame.mixer.Sound('data/slodrum.mp3'),
        }
        self.music['base'].set_volume(0.5)
        
        for item in self.music:
            self.music[item].play(-1)
        
        self.sfx['ambience'].set_volume(0.2)
        self.sfx['shoot'].set_volume(0.4)
        self.sfx['hit'].set_volume(0.8)
        self.sfx['dash'].set_volume(0.3)
        self.sfx['jump'].set_volume(0.7)
        
        self.channelnums = []
        i = 0
        for item in self.music:
            self.channelnums.append(pygame.mixer.Channel(i))
            i += 1
        
        for item in self.sfx:
            self.channelnums.append(pygame.mixer.Channel(i))
            i += 1
        
        self.channels = {}
        for key in self.sfx:
            for value in self.channelnums:
                self.channels[key] = value
                self.channelnums.remove(value)
                break
        for key in self.music:
            for value in self.channelnums:
                self.channels[key] = value
                self.channelnums.remove(value)
                break
        
        self.fades = []
        
        
    def fadebetween(self, musicid1=None, musicid2=None, timeinms=0, goalvolumeout=0.0, goalvolumein=1.0):
        #musicid1 is fading out
        #musicid2 is fading in
        if not(musicid1 == None):
            self.channels[musicid1].fadeout(timeinms)
        if not(musicid2 == None):
            self.channels[musicid2].set_volume(goalvolumein)
            self.channels[musicid2].play(self.music[musicid2],-1, fade_ms=timeinms)
        
        #self.channels[musicid2].set_volume(0.0)
        
        #hin = ((self.channels[musicid1].get_volume() - goalvolumeout) / timeinms)
        #out = ((self.channels[musicid2].get_volume() - goalvolumein) / timeinms)
        #print(' . ')
        #print(hin)
        #print(' . ')
        #print(out)
        #self.fades.append([musicid1, hin, goalvolumein, musicid2, out, goalvolumeout])
        #self.channels[musicid1].play(self.music[musicid1], -1)
        #self.channels[musicid2].play(self.music[musicid2], -1)
    
    def update(self):
        
        
        
        for fade in self.fades:
            if self.channels[fade[0]].get_volume() == fade[2]:
                self.fades.remove(fade)
            else:
                self.channels[fade[0]].set_volume((self.channels[fade[0]].get_volume() - fade[1]))
                self.channels[fade[3]].set_volume((self.channels[fade[3]].get_volume() - fade[4]))
                
        self.setvolume(self.game.volume)
        
        
    
    def setvolume(self, volumetoset):
        if volumetoset != 0:
            for item in self.sfx:
                self.sfx[item].set_volume((self.channels[item].get_volume() * (volumetoset / 100)))
            for item in self.music:
                self.music[item].set_volume((self.channels[item].get_volume() * (volumetoset / 100)))
                
class Sfx(MusicManager):
    
    def __init__(self):
        super().__init__()
        
class Soundtrack(MusicManager):
    
    def __init__(self):
        super().__init__()
        
        
class SoundSource(object):
    def __init__(self, sound, pos, max_volume, audible_range):
        """        
        sound: a pygame.Sound object
        pos: x, y position for calculating distance to listener
        max_volume: float between 0 and 1 (inclusive), this is the volume when 
                             the distance to the listener is 0
        audible_range: int or float, distance at which sound begins playing (at volume 0)
        """
        self.sound = [sound].copy()
        self.sound = self.sound[0]
        self.pos = pos
        self.max_volume = max_volume
        self.audible_range = audible_range
        self.active = False
        
    def update(self, listener, pos=[]):
        """        
        listener: the position of the listening device
        pos: x, y position for calculating distance to listener
        """
        active = False
        distance_to_listener = abs(math.dist(listener, pos))
        if distance_to_listener <= self.audible_range:
            active = True
            volume = self.max_volume * (1 - (distance_to_listener / self.audible_range))
            #print(volume)
            self.sound.set_volume(volume)
        else:
            active = False
            self.sound.stop()
        
    def play(self):
        self.sound.play()  
pygame.init()
pygame.mixer.init()

clock = pygame.time.Clock()
rt = Realtime_Audio()
while True:
    rt.update()
    clock.tick(60)