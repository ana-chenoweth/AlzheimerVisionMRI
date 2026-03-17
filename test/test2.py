import SimpleITK as sitk
import matplotlib.pyplot as plt
import numpy as np
import os

dicom_dir = "002_S_0413/Accelerated_Sagittal_MPRAGE/2017-06-21_13_23_38.0/I863056"

reader = sitk.ImageSeriesReader()
series_ids = reader.GetGDCMSeriesIDs(dicom_dir)

if not series_ids:
    raise RuntimeError(f"No se encontraron series DICOM en: {dicom_dir}")

series_files = reader.GetGDCMSeriesFileNames(dicom_dir, series_ids[0])
reader.SetFileNames(series_files)

image = reader.Execute()
volume = sitk.GetArrayFromImage(image)  # [slices, height, width]

print("Shape del volumen:", volume.shape)
"""
(176, 256, 256)

176 cortes del cerebro

cada corte de 256x256 píxeles

"""
print("Tipo de dato:", volume.dtype)
print("Valor min:", volume.min())
print("Valor max:", volume.max())

mid = volume.shape[0] // 2 #CORTE CENTRAL

plt.imshow(volume[mid], cmap="gray")
plt.title("Corte central")
plt.axis("off")
plt.savefig("corte_central.png", bbox_inches="tight")
print("Imagen guardada como corte_central.png")