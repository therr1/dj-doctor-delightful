
import numpy as np  
import colorsys 


MIN_BUCKET = 50 #hz
MAX_BUCKET = 20000 #hz
NUM_LIGHTS = 14 #number of lights around the room
MAX_AMPLITUDE = 1

#rgb_val is between 0 and 255
def val_to_hex_str(rgb_val):
    representation = ((str)(hex(rgb_val)))[2:]
    if (len(representation) == 1):
        representation = "0" + representation
    return representation

class Algorithm:
    #fft_data is a time series representation of the fft
    def __init__(self, fft_data):
        self.fft_data = fft_data

    #equalizer is the most simple algorithm we might use, it simply just
    #displays the values of the fft in a circle of colors
    def equalizer(self):
        num_buckets = self.fft_data.size
        final_rgb_triples = np.zeros((NUM_LIGHTS,3))
        # print(final_rgb_triples)
        # print final_rgb_triples 

        light_amplitude_values = np.zeros(NUM_LIGHTS)
        for i in range(num_buckets):
            #populate light_amplitude_values with the result from the fft. 
            for j in range((int)(i*1.0*NUM_LIGHTS/num_buckets),(int)((i+1)*1.0*NUM_LIGHTS/num_buckets)):
                light_amplitude_values[j] = self.fft_data[i]

        final_hex_vals = np.chararray(NUM_LIGHTS,itemsize=7)
        for i in range(NUM_LIGHTS):
            (r, g, b) = colorsys.hsv_to_rgb(1.0*i/NUM_LIGHTS, 1.0, light_amplitude_values[i]*1.0/MAX_AMPLITUDE)
            (R, G, B) = int(255 * r), int(255 * g), int(255 * b)
            hexval = "#" + val_to_hex_str(R) + val_to_hex_str(G) + val_to_hex_str(B)
            final_hex_vals[i] = hexval
        # maxd = 1
        # (r, g, b) = colorsys.hsv_to_rgb(float(depth) / maxd, 1.0, 1.0)
        # rgb = int(255 * r), int(255 * g), int(255 * b)
        # print rgb 
        return final_hex_vals



data = np.array([0.5,0.6,0.7])
algo = Algorithm(data)
print algo.equalizer()