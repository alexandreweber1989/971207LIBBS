@echo off
cd /d "C:\Users\alew1\Desktop\Novo Relatório\971207LIBBS"

echo Atualizando repositório...

git add .
git commit -m "Atualização automática - %DATE% %TIME%"
git push origin main

echo Atualização concluída!
pause