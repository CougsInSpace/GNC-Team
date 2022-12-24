from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
import math

sample_rate, data = wavfile.read("go cougs mono.wav")
print("sample_rate " + str(sample_rate))

# plt.plot(data)
# plt.show()

# FM MODULATION

# dataInt = np.trapz(data)
dataInt = np.zeros(data.size)
for n in range(1, data.size):
    dataInt[n] = dataInt[n - 1] + data[n]

print(dataInt)
# plt.plot(dataInt)
# plt.show()
data1 = np.add(np.divide(dataInt, 2*max(abs(dataInt))), .5)
dataFinal = np.multiply(data1, 360)



# AM MODULATION

# # print(max(data))
# print(2**.5)
# dataFinal = np.add(np.divide(data, max(abs(data))*2), .5)
# dataFinal = np.multiply(np.divide(dataFinal, 2**.5), 1023)
# # dataFinal = np.multiply(np.add(np.divide(data, max(abs(data))*(2**.5)*2), 1), 1023)
plt.plot(dataFinal)
plt.show()
# print(dataFinal.size)






string = "{"
for n in range(dataFinal.size):
    string += str(int(dataFinal[n])) + ","

file = open("IQArrayFM.txt", "w")
file.write(string)
file.close()


