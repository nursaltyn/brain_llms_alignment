@echo off
setlocal enabledelayedexpansion

set "gpt=perceived"
set "num_stories=10"

for /L %%s in (2, 1, 8) do (
    set "subject=0%%s"
    for /L %%i in (0, 1, 11) do (
        python train_EM_speech_network.py --subject !subject! --gpt !gpt! --layer %%i --num_stories !num_stories!
    )
)