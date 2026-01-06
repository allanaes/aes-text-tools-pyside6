## Setup VENV
```
python -m venv .venv
```

## Activate VENV (Contoh: Windows -> PowerShell)
```
.\.venv\Scripts\Activate.ps1
```

## Install Requirements
```
pip install -r requirements.txt
```

## Run App / Develop
```
python app.py
```

## Deploy
Rename `pysidedeploy.spec.example` menjadi `pysidedeploy.spec`

Run:
```
pyside6-deploy -c pysidedeploy.spec
```

Deployment menghasilkan single executable. Salin folder `includes` bersama single executable tersebut dan aplikasi sudah dapat digunakan secara portable. Folder `includes` berisi file `replacements.json` yang berisi dictionary untuk mereplace kata atau frasa tertentu dalam fungsi Proper Text dan Sentence Text. Daftar istilah dapat ditambah sesuai kebutuhan. Urutan dictionary sangat berpengaruh terhadap hasil replace.


## Misc
Convert .qrc to .py
```
pyside6-rcc resources.qrc -o resources.py
```
