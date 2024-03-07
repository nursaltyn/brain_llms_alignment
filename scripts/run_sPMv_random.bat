@echo off
setlocal enabledelayedexpansion

set "gpt=perceived"
set "area=roi_mask_sPMv"
set "num_stories=10"

for /L %%s in (1, 1, 3) do (
    set "subject=0%%s"
    for /L %%i in (0, 1, 11) do (
        python train_EM_random.py --subject !subject! --gpt !gpt! --layer %%i --area !area! --num_stories !num_stories!
    )
)