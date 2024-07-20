# Copyright Epic Games, Inc. All Rights Reserved.
import unreal
import argparse
import sys
import os
import json


def create_performance_asset(path_to_identity : str, path_to_capture_data : str, save_performance_location : str) -> unreal.MetaHumanPerformance:
    
    capture_data_asset = unreal.load_asset(path_to_capture_data)
    identity_asset = unreal.load_asset(path_to_identity)
    performance_asset_name = "{0}_Performance".format(capture_data_asset.get_name())

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    performance_asset = asset_tools.create_asset(asset_name=performance_asset_name, package_path=save_performance_location, 
                                                 asset_class=unreal.MetaHumanPerformance, factory=unreal.MetaHumanPerformanceFactoryNew())

    # Use this style as set_editor_property doesn't trigger the PostEditChangeProperty required to setup the Performance asset
    performance_asset.set_editor_property("identity", identity_asset)
    performance_asset.set_editor_property("footage_capture_data", capture_data_asset)

    return performance_asset


def process_shot(performance_asset : unreal.MetaHumanPerformance, export_level_sequence : bool, export_sequence_location : str,
                 path_to_meta_human_target : str, start_frame : int = None, end_frame : int = None):
    
    if start_frame is not None:
        performance_asset.set_editor_property("start_frame_to_process", start_frame)

    if end_frame is not None:
        performance_asset.set_editor_property("end_frame_to_process", end_frame)

    #Setting process to blocking will make sure the action is executed on the main thread, blocking it until processing is finished
    process_blocking = True
    performance_asset.set_blocking_processing(process_blocking)

    # Register a callback that is called after the shot was processed
    def shot_processing_finished():
        unreal.log("Finished processing shot for Performance '{0}'".format(performance_asset.get_name()))
        performance_asset.on_processing_finished_dynamic.remove_callable(shot_processing_finished)

        if export_level_sequence is True:
            run_level_sequence_export(performance_asset, export_sequence_location, path_to_meta_human_target)

    # Register a callback for when the pipeline finishes running
    performance_asset.on_processing_finished_dynamic.add_callable(shot_processing_finished)

    unreal.log("Starting MH pipeline for '{0}'".format(performance_asset.get_name()))
    startPipelineError = performance_asset.start_pipeline()
    if startPipelineError is unreal.StartPipelineErrorType.NONE:
        unreal.log("Finished MH pipeline for '{0}'".format(performance_asset.get_name()))
    elif startPipelineError is unreal.StartPipelineErrorType.TOO_MANY_FRAMES:
        unreal.log("Too many frames when starting MH pipeline for '{0}'".format(performance_asset.get_name()))
    else:
        unreal.log("Unknown error starting MH pipeline for '{0}'".format(performance_asset.get_name()))


def run_level_sequence_export(performance_asset : unreal.MetaHumanPerformance, export_sequence_location : str, path_to_target_meta_human : str = ''):
    
    performance_asset_name = performance_asset.get_name()
    unreal.log("Exporting animation sequence for Performance '{0}'".format(performance_asset_name))

    export_settings = unreal.MetaHumanPerformanceExportAnimationSettings()
    # Enable or disable to export the head rotation as curve data
    export_settings.enable_head_movement = False # default is False
    # This hides the dialog where the user can select the path to write the anim sequence
    export_settings.show_export_dialog = False
    # Use name_prefix to set a prefix to be added to the anim sequence name
    # Use export_range to select the whole sequence or only the processing range
    export_settings.export_range = unreal.PerformanceExportRange.PROCESSING_RANGE
    # Export the animation sequence from the performance using the given settings
    anim_sequence: unreal.AnimSequence = unreal.MetaHumanPerformanceExportUtils.export_animation_sequence(performance_asset, export_settings)
    unreal.log("Exported Anim Sequence {0}".format(anim_sequence.get_name()))

    unreal.log("Exporting level sequence for performance '{0}'".format(performance_asset_name))
    level_sequence_export_settings = unreal.MetaHumanPerformanceExportLevelSequenceSettings()
    level_sequence_export_settings.show_export_dialog = False
    # if the path and name are not set, will use the performance as a base name
    level_sequence_export_settings.package_path = export_sequence_location
    level_sequence_export_settings.asset_name = "LevelSequence_{0}".format(performance_asset_name)

    # customize various export settings
    level_sequence_export_settings.export_video_track = True
    level_sequence_export_settings.export_depth_track = False
    level_sequence_export_settings.export_audio_track = True
    level_sequence_export_settings.export_image_plane = True
    level_sequence_export_settings.export_camera = True
    level_sequence_export_settings.export_identity = True
    level_sequence_export_settings.enable_meta_human_head_movement = True
    level_sequence_export_settings.export_control_rig_track = True
    level_sequence_export_settings.export_transform_track = False
    level_sequence_export_settings.export_range = unreal.PerformanceExportRange.WHOLE_SEQUENCE
    level_sequence_export_settings.enable_meta_human_head_movement = True

    # Set a MetaHuman blueprint to target when exporting the Level Sequence
    if len(path_to_target_meta_human) != 0 :
        target_MetaHuman_BP_asset: unreal.Blueprint = unreal.load_asset(path_to_target_meta_human)
        level_sequence_export_settings.target_meta_human_class = target_MetaHuman_BP_asset.generated_class()

    exported_level_sequence: unreal.LevelSequence = unreal.MetaHumanPerformanceExportUtils.export_level_sequence(performance=performance_asset, export_settings=level_sequence_export_settings)
    unreal.log("Exported Level Sequence {0}".format(exported_level_sequence.get_name()))

    return exported_level_sequence


def run(end_frame):
    
    #load into the metahuman identity and capture footage, then output a metahuman performance
    performance_asset = create_performance_asset(
        path_to_identity="/Game/MetaHumans/vasilisa_MI2",
        path_to_capture_data="/Game/MetaHumans/va637_Ingested/006Vasilisa_637",
        save_performance_location="/Game/Test/")
    
    #process the metahuman performance and export the animation sequence
    process_shot(
        performance_asset=performance_asset,
        export_level_sequence=True,
        export_sequence_location="/Game/Test/",
        path_to_meta_human_target="/Game/MetaHumans/Cooper",
        start_frame=0,
        end_frame=end_frame)

    

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
            run(end_frame)