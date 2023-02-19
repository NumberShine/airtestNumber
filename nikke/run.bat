echo 添加 bat 环境变量
set regpath=HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment
set evname=PYTHONPATH
set batpath=F:\Code\airtest
reg add "%regpath%" /v %evname% /d %batpath% /f
python F:\Code\airtest\nikke\first.py
pause

