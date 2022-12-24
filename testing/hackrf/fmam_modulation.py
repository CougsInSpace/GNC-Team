from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
import math

sample_rate, data = wavfile.read("go cougs mono48.wav")
print("sample_rate " + str(sample_rate))

dac_max = 1024

# Normalize audio to -1 to 1
data = data / max(abs(data)) * 1 #+ np.cos(np.pi*2*3000*np.arange(data.size)/sample_rate) * 1

# Transformation -1 to 1 to DAC codes (0 - 1023)
dac =  lambda x: np.clip(dac_max * (x / 2 + 0.5), 0, dac_max - 1)

# AM DAC codes
data_am = dac(data)
_, subplots = plt.subplots(3, 1)
subplots[0].plot(data_am)
subplots[0].set_title("AM DAC Codes")

# FM 
# Step 1: integrate
data_int = np.zeros(data.size)
data_int[0] = data[0]
for i in range(1, data.size):
  data_int[i] = data_int[i - 1] + data[i]

# Step 2: trig
data_fm_i = np.cos(data_int/(2*np.pi)) * 1
data_fm_q = np.sin(data_int/(2*np.pi)) * 1

# Step 3: Convert to DAC Codes
data_fm_i = dac(data_fm_i)
data_fm_q = dac(data_fm_q)


with open("IQArray.txt", "w", encoding="utf-8") as file:
  file.write(f"static constexpr uint16_t MSG_DAC_AM_IQ[{data.size}] = {{")
  file.write(",".join([str(int(v)) for v in data_am]))
  file.write("};\n")

  file.write(f"static constexpr uint16_t MSG_DAC_FM_I[{data.size}] = {{")
  file.write(",".join([str(int(v)) for v in data_fm_i]))
  file.write("};\n")
  
  file.write(f"static constexpr uint16_t MSG_DAC_FM_Q[{data.size}] = {{")
  file.write(",".join([str(int(v)) for v in data_fm_q]))
  file.write("};\n")

subplots[1].plot(data_fm_i)
subplots[1].set_title("FM DAC Codes - I")
subplots[2].plot(data_fm_q)
subplots[2].set_title("FM DAC Codes - Q")
plt.tight_layout()
# plt.show()


