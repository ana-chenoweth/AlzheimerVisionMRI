# AlzheimerVisionMRI
Early detection of Alzheimer’s disease from structural MRI using deep learning and self-supervised representations

Crear entorno conda:

`conda create -n adni3d python=3.10`

`source activate adni3d`

`pip install numpy pandas matplotlib scipy scikit-image scikit-learn SimpleITK nibabel pydicom tqdm monai`

`pip install torch torchvision torchaudio`

Verificar:
`python -c "import torch; print(torch.__version__)"`

`python -c "import SimpleITK; print('OK')"`
