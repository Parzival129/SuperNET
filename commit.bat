@ECHO OFF
color 0a
ECHO COMMITING STFFF

git add .
set /p message=Commit message:
git commit -m %message%
git push -u origin master
