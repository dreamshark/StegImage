import numpy as np
from steganogan import SteganoGAN
from steganogan.loader import DataLoader
from steganogan.encoders import BasicEncoder, DenseEncoder
from steganogan.decoders import BasicDecoder, DenseDecoder
from steganogan.critics import BasicCritic

steganogan = SteganoGAN.load(architecture=None, path='steg/final.steg', cuda=True, verbose=True)

print(steganogan.decode('output.png'))
