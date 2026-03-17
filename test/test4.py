import SimpleITK as sitk
import matplotlib.pyplot as plt

dicom_dir = "002_S_0413/Accelerated_Sagittal_MPRAGE/2017-06-21_13_23_38.0/I863056"

reader = sitk.ImageSeriesReader()
series_ids = reader.GetGDCMSeriesIDs(dicom_dir)
series_files = reader.GetGDCMSeriesFileNames(dicom_dir, series_ids[0])
reader.SetFileNames(series_files)

image = reader.Execute()
volume = sitk.GetArrayFromImage(image)

for i in range(0, volume.shape[0], 10):
    plt.imshow(volume[i], cmap="gray")
    plt.title(f"Corte {i}")
    plt.axis("off")
    plt.show()