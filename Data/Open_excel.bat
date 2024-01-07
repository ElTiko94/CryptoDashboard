@echo off

rem Définir les variables pour les chemins de fichiers
set HISTORIQUE_ACHATS="Data\Historique d'achats.xlsx"
set VISION_GENERAL="Data\Vision General.xlsx"


rem Appeler la fonction d'ouverture des fichiers
call :ouvrirFichier %HISTORIQUE_ACHATS% "Historique d achats.xlsx"
call :ouvrirFichier %VISION_GENERAL% "Vision General.xlsx"
"C:\Program Files\Git\git-bash.exe" "Data\push_Changes.sh"

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