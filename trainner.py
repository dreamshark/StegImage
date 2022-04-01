import numpy as np #numpy is used for a parameter input
from steganogan import SteganoGAN
from steganogan.loader import DataLoader
from steganogan.encoders import BasicEncoder, DenseEncoder
from steganogan.decoders import BasicDecoder, DenseDecoder
from steganogan.critics import BasicCritic

# Load the data
train = DataLoader('D:/dataset/train', limit=np.inf, shuffle=True, batch_size=4)
validation = DataLoader('D:/dataset/val', limit=np.inf, shuffle=True, batch_size=4)

# Create the SteganoGAN instance
steganogan = SteganoGAN(1, BasicEncoder, BasicDecoder, BasicCritic, hidden_size=32, cuda=True, verbose=True)

# Fit on the given data
steganogan.fit(train, validation, epochs=5)

# Save the fitted model
steganogan.save('test1.steg')