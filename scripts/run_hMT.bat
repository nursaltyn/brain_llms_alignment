@echo off
setlocal enabledelayedexpansion

set "gpt=perceived"
set "area=roi_mask_hMT"
set "num_stories=10"

for /L %%s in (2, 1, 9) do (
    set "subject=0%%s"
    for /L %%i in (0, 1, 11) do (
        python train_EM_swapped.py --subject !subject! --gpt !gpt! --layer %%i --area !area! --num_stories !num_stories!
    )
)