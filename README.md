# Unreal Engine UIvision
Using UI vision RPA to achieve the automation of the animator performance part in Unreal Engine  (It includes files: CPU_usage.ps1, UnrealEngine_UI_automation.json, UnrealEngine_automation_demo.mp4)
  
1. The json file is the commands flow of the UI vision RPA
2. The UI vision RPA needs to set up by following the commands
3. CPU usage powershell script is used to detect the CPU usage situation (if CPU usage > certain range: return FALSE; Else: return TRUE)
4. Run the macro on the UI vision RPA to automate the process
!!!The above method is not robust since it uses the second platform!!!  

# Unreal Engine Python Script
Another method to solve the problem is to use python script. (It includes files: PythonDemo_UE.mp4, UE_MetahumanPerformance)  
It will choose the video footage and metahuman identity first, then create the performance asset, then adjust the setting of the performance, then process the performance and output animation sequence to the destination path.

# Example
<img width="283" alt="image" src="https://github.com/JerryTseee/UnrealEngine_UIvision/assets/126223772/e92d193a-7344-441c-82a0-45927ea84862">
<img width="259" alt="image" src="https://github.com/JerryTseee/UnrealEngine_UIvision/assets/126223772/69e2b0b2-2e9c-42b8-83b7-fbb36bdec7ce">
