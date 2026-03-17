import SimpleITK as sitk
import matplotlib.pyplot as plt
import numpy as np

dicom_dir = "002_S_0413/Accelerated_Sagittal_MPRAGE/2017-06-21_13_23_38.0/I863056"

reader = sitk.ImageSeriesReader()
series_ids = reader.GetGDCMSeriesIDs(dicom_dir)
series_files = reader.GetGDCMSeriesFileNames(dicom_dir, series_ids[0])
reader.SetFileNames(series_files)

image = reader.Execute()
volume = sitk.GetArrayFromImage(image)   # shape: [slices, height, width]

print("Shape del volumen:", volume.shape)

# Mostrar un corte central
mid = volume.shape[0] // 2
plt.imshow(volume[mid], cmap="gray")
plt.title("Corte central")
plt.axis("off")
plt.show()