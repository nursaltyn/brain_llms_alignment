@echo off

echo Running temporal network
call run_temporal_network.bat

echo Running occipital network
call run_occipital_network.bat

echo Running parietal network
call run_parietal_network.bat

Rem echo Running speech network
Rem call run_speech_network.bat
