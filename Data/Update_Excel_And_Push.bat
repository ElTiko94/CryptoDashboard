@echo off

rem Définir les variables pour les chemins de fichiers
set DATA_PY="C:\Users\Tiko\Desktop\Tiko\investissement\Gestion de crypto\Data\getData.py"
set HISTORIQUE_ACHATS="C:\Users\Tiko\Desktop\Tiko\investissement\Gestion de crypto\Data\Historique d'achats.xlsx"
set VISION_GENERAL="C:\Users\Tiko\Desktop\Tiko\investissement\Gestion de crypto\Data\Vision General.xlsx"

rem Exécuter getData.py
echo Exécution de getData.py...
start "getData.py" %DATA_PY%
TIMEOUT 20

rem Pousser les modif sur git
"C:\Program Files\Git\git-bash.exe" "C:\Users\Tiko\Desktop\Tiko\investissement\Gestion de crypto\Data\push_Changes.sh"
