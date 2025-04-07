@echo off
cd /d "C:\Users\alew1\Desktop\Novo Relatório\971207LIBBS"

echo ========================================
echo Iniciando atualização do repositório...
echo ========================================

:: Força a inclusão da planilha, mesmo que esteja no .gitignore
git add "DADOS GERAIS - PBI.xlsx" --force

:: Adiciona todos os outros arquivos
git add .

:: Cria commit com data e hora
git commit -m "Atualização automática - %DATE% %TIME%"

:: Envia para o GitHub
git push origin main

echo ========================================
echo Atualização concluída com sucesso!
echo ========================================
pause