import unreal
import argparse
import sys
import os
import json
import tkinter as tk
from tkinter import filedialog


def create_performance_asset(path_to_identity : str, path_to_capture_data : str, save_performance_location : str) -> unreal.MetaHumanPerformance:
    
    capture_data_asset = unreal.load_asset(path_to_capture_data)
    identity_asset = unreal.load_asset(path_to_identity)
    performance_asset_name = "{0}_Performance".format(capture_data_asset.get_name())

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    performance_asset = asset_tools.create_asset(asset_name=performance_asset_name, package_path=save_performance_location, 
                                                 asset_class=unreal.MetaHumanPerformance, factory=unreal.MetaHumanPerformanceFactoryNew())

    
    performance_asset.set_editor_property("identity", identity_asset)# load into the identity setting
    performance_asset.set_editor_property("footage_capture_data", capture_data_asset)# load into the capture footage setting

    return performance_asset



def run_animation_export(performance_asset : unreal.MetaHumanPerformance):
    
    performance_asset_name = performance_asset.get_name()# this is the name of the animation sequence
    unreal.log("Exporting animation sequence for Performance '{0}'".format(performance_asset_name))

    export_settings = unreal.MetaHumanPerformanceExportAnimationSettings()
    export_settings.enable_head_movement = False# Enable or disable to export the head rotation
    export_settings.show_export_dialog = False
    export_settings.export_range = unreal.PerformanceExportRange.PROCESSING_RANGE
    anim_sequence: unreal.AnimSequence = unreal.MetaHumanPerformanceExportUtils.export_animation_sequence(performance_asset, export_settings)
    unreal.log("Exported Anim Sequence {0}".format(anim_sequence.get_name()))




def process_shot(performance_asset : unreal.MetaHumanPerformance, export_level_sequence : bool, export_sequence_location : str,
                 path_to_meta_human_target : str, start_frame : int = None, end_frame : int = None):
    
    if start_frame is not None:
        performance_asset.set_editor_property("start_frame_to_process", start_frame)

    if end_frame is not None:
        performance_asset.set_editor_property("end_frame_to_process", end_frame)

    #Setting process to blocking will make sure the action is executed on the main thread, blocking it until processing is finished
    process_blocking = True
    performance_asset.set_blocking_processing(process_blocking)

    unreal.log("Starting MH pipeline for '{0}'".format(performance_asset.get_name()))
    startPipelineError = performance_asset.start_pipeline()
    if startPipelineError is unreal.StartPipelineErrorType.NONE:
        unreal.log("Finished MH pipeline for '{0}'".format(performance_asset.get_name()))
    elif startPipelineError is unreal.StartPipelineErrorType.TOO_MANY_FRAMES:
        unreal.log("Too many frames when starting MH pipeline for '{0}'".format(performance_asset.get_name()))
    else:
        unreal.log("Unknown error starting MH pipeline for '{0}'".format(performance_asset.get_name()))

    #export the animation sequence
    run_animation_export(performance_asset)

    # finally return the name of animation sequence
    return performance_asset.get_name()




def run(end_frame):
    
    #load into the metahuman identity and capture footage, then output a metahuman performance
    performance_asset = create_performance_asset(
        path_to_identity="/Game/MetaHumans/vasilisa_MI2",
        path_to_capture_data="/Game/MetaHumans/va26_Ingested/006Vasilisa_26",
        save_performance_location="/Game/Test/")
    
    #process the metahuman performance and export the animation sequence
    animation_name = process_shot(
        performance_asset=performance_asset,
        export_level_sequence=True,
        export_sequence_location="/Game/Test/",
        path_to_meta_human_target="/Game/MetaHumans/Cooper",
        start_frame=0,
        end_frame=end_frame)
    
    return animation_name







#path that contains video data, start to process performance
path = "F:\\Jerry\\Vasilisa"
for i in os.listdir(path):
    set_path = os.path.join(path, i)
    if os.path.isdir(set_path):
        json_file_path = os.path.join(set_path, "take.json")
        if os.path.isfile(json_file_path):
            with open(json_file_path, "r") as file:
                data = json.load(file)
            end_frame = data["frames"]
            end_frame = end_frame // 2 + 1
            animation_name = run(end_frame)
            print("The performance process is done!")
            print("The name of the animation sequence is: " + str(animation_name))
            print("Done with the first part")
