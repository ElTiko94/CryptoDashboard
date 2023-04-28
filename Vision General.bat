@echo off

rem Définir les variables pour les chemins de fichiers
set DATA_PY="C:\Users\Tiko\Desktop\Tiko\investissement\Gestion de crypto\Data\getData.py"
set HISTORIQUE_ACHATS="C:\Users\Tiko\Desktop\Tiko\investissement\Gestion de crypto\Data\Historique d'achats.xlsx"
set VISION_GENERAL="C:\Users\Tiko\Desktop\Tiko\investissement\Gestion de crypto\Data\Vision General.xlsx"

rem Exécuter getData.py
echo Exécution de getData.py...
start "getData.py" %DATA_PY%
TIMEOUT 4

rem Appeler la fonction d'ouverture des fichiers
call :ouvrirFichier %HISTORIQUE_ACHATS% "Historique d achats.xlsx"
call :ouvrirFichier %VISION_GENERAL% "Vision General.xlsx"
"C:\Program Files\Git\git-bash.exe" "C:\Users\Tiko\Desktop\Tiko\investissement\Gestion de crypto\Data\push_Changes.sh"

goto :eof

rem Fonction pour ouvrir un fichier s'il existe
:ouvrirFichier
if exist %1 (
    echo Ouverture de %2...
    start %2 %1
) else (
    echo Fichier %2 introuvable.
)
goto :eof