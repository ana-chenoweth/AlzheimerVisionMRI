import SimpleITK as sitk
import matplotlib.pyplot as plt

dicom_dir = "002_S_0413/Accelerated_Sagittal_MPRAGE/2017-06-21_13_23_38.0/I863056"

reader = sitk.ImageSeriesReader()
series_ids = reader.GetGDCMSeriesIDs(dicom_dir)
series_files = reader.GetGDCMSeriesFileNames(dicom_dir, series_ids[0])
reader.SetFileNames(series_files)

image = reader.Execute()
volume = sitk.GetArrayFromImage(image)

print("Shape:", volume.shape)

indices = [20, 40, 60, 80, 100, 120]

fig, axes = plt.subplots(2, 3, figsize=(10, 7))

for ax, idx in zip(axes.ravel(), indices):
    ax.imshow(volume[idx], cmap="gray")
    ax.set_title(f"Corte {idx}")
    ax.axis("off")

plt.tight_layout()
plt.show()