from pathlib import Path
import os
import numpy as np
import pandas as pd
import torch
import SimpleITK as sitk

BASE_DIR = Path("/lustre/home/estudiante_93/alzheimer_project")
ADNI_DIR = BASE_DIR / "ADNI"
NIFTI_DIR = BASE_DIR / "nifti"
TENSOR_DIR = BASE_DIR / "tensors_pt"
METADATA_DIR = BASE_DIR / "metadata"

NIFTI_DIR.mkdir(exist_ok=True)
TENSOR_DIR.mkdir(exist_ok=True)
METADATA_DIR.mkdir(exist_ok=True)

MAX_SUBJECTS = None   # cambia a None para procesar todos

def find_leaf_dicom_dirs(root: Path):
    dicom_dirs = []
    for current_root, dirs, files in os.walk(root):
        if any(f.lower().endswith(".dcm") for f in files):
            dicom_dirs.append(Path(current_root))
    return sorted(dicom_dirs)

def normalize_minmax(volume: np.ndarray) -> np.ndarray:
    volume = volume.astype(np.float32)
    vmin = volume.min()
    vmax = volume.max()
    return (volume - vmin) / (vmax - vmin + 1e-8)

def process_subject(dicom_dir: Path):
    subject_id = dicom_dir.parts[-4]

    reader = sitk.ImageSeriesReader()
    series_ids = reader.GetGDCMSeriesIDs(str(dicom_dir))
    if not series_ids:
        raise RuntimeError(f"No series DICOM en {dicom_dir}")

    series_files = reader.GetGDCMSeriesFileNames(str(dicom_dir), series_ids[0])
    reader.SetFileNames(series_files)
    image = reader.Execute()

    volume = sitk.GetArrayFromImage(image)  # (D, H, W)
    volume_norm = normalize_minmax(volume)

    tensor = torch.from_numpy(volume_norm).unsqueeze(0)  # (1, D, H, W)

    nifti_path = NIFTI_DIR / f"{subject_id}.nii.gz"
    pt_path = TENSOR_DIR / f"{subject_id}.pt"

    sitk.WriteImage(image, str(nifti_path))
    torch.save(tensor, pt_path)

    return {
        "subject_id": subject_id,
        "dicom_dir": str(dicom_dir),
        "nifti_path": str(nifti_path),
        "pt_path": str(pt_path),
        "depth": int(volume.shape[0]),
        "height": int(volume.shape[1]),
        "width": int(volume.shape[2]),
        "spacing_x": float(image.GetSpacing()[0]),
        "spacing_y": float(image.GetSpacing()[1]),
        "spacing_z": float(image.GetSpacing()[2]),
        "origin_x": float(image.GetOrigin()[0]),
        "origin_y": float(image.GetOrigin()[1]),
        "origin_z": float(image.GetOrigin()[2]),
        "dtype_original": str(volume.dtype),
        "min_intensity": float(volume.min()),
        "max_intensity": float(volume.max()),
    }

def main():
    dicom_dirs = find_leaf_dicom_dirs(ADNI_DIR)
    print(f"Se encontraron {len(dicom_dirs)} carpetas DICOM finales.")

    if MAX_SUBJECTS is not None:
        dicom_dirs = dicom_dirs[:MAX_SUBJECTS]
        print(f"Procesando solo {len(dicom_dirs)} sujetos de prueba.")

    records = []

    for i, dicom_dir in enumerate(dicom_dirs, start=1):
        try:
            print(f"[{i}/{len(dicom_dirs)}] Procesando: {dicom_dir}")
            rec = process_subject(dicom_dir)
            records.append(rec)
            print(f"  OK -> {rec['subject_id']} shape=({rec['depth']}, {rec['height']}, {rec['width']})")
        except Exception as e:
            print(f"  ERROR en {dicom_dir}: {e}")

    df = pd.DataFrame(records)
    out_csv = METADATA_DIR / "metadata_test.csv"
    df.to_csv(out_csv, index=False)
    print(f"Metadata guardada en: {out_csv}")

if __name__ == "__main__":
    main()
