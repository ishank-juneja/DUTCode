#!/bin/bash
# Some other videos in dataset are .mp4
for video in in_paths = ../dataset/spherical-robot/*.mp4; do
	# Checks if a file like instance
	# actually exists or is just a glob
	[ -e "$video" ] || continue
	# echo $out_name
	# Slow step so check if output file already exists
	out_name="../results-new/DIFRINT/spherical-robot-out/$(basename "$video" .mp4)_DIFRINT_out.avi"
	if [ -f "$out_name" ]; then
		echo -e $"Results for video $video exist, ... skipping run\n"
	else
	echo -e $"Currently running on $video\n"
  python3 scripts/DIFRINTStabilizer.py -i "$video" -o "$out_name" --modelPath="ckpt/DIFNet2.pth" --cuda
	fi
done

for video in in_paths = ../dataset/skydio/*.mp4; do
	# Checks if a file like instance
	# actually exists or is just a glob
	[ -e "$video" ] || continue
	# echo $out_name
	# Slow step so check if output file already exists
	out_name="../results-new/DIFRINT/skydio-out/$(basename "$video" .mp4)_DIFRINT_out.avi"
	if [ -f "$out_name" ]; then
		echo -e $"Results for video $video exist, ... skipping run\n"
	else
	echo -e $"Currently running on $video\n"
  python3 scripts/DIFRINTStabilizer.py -i "$video" -o "$out_name" --modelPath="ckpt/DIFNet2.pth" --cuda
	fi
done

for video in in_paths = ../dataset/DeepStab/unstable/*.avi; do
	# Checks if a file like instance
	# actually exists or is just a glob
	[ -e "$video" ] || continue
	# echo $out_name
	# Slow step so check if output file already exists
	out_name="../results-new/DIFRINT/DeepStab/$(basename "$video" .avi)_DIFRINT_out.avi"
	if [ -f "$out_name" ]; then
		echo -e $"Results for video $video exist, ... skipping run\n"
	else
	echo -e $"Currently running on $video\n"
  python3 scripts/DIFRINTStabilizer.py -i "$video" -o "$out_name" --modelPath="ckpt/DIFNet2.pth" --cuda
	fi
done

for video in in_paths = ../dataset/Crowd/unstable/*.avi; do
	# Checks if a file like instance
	# actually exists or is just a glob
	[ -e "$video" ] || continue
	# echo $out_name
	# Slow step so check if output file already exists
	out_name="../results-new/DIFRINT/Crowd/$(basename "$video" .avi)_DIFRINT_out.avi"
	if [ -f "$out_name" ]; then
		echo -e $"Results for video $video exist, ... skipping run\n"
	else
	echo -e $"Currently running on $video\n"
  python3 scripts/DIFRINTStabilizer.py -i "$video" -o "$out_name" --modelPath="ckpt/DIFNet2.pth" --cuda
	fi
done

for video in in_paths = ../dataset/Parallax/unstable/*.avi; do
	# Checks if a file like instance
	# actually exists or is just a glob
	[ -e "$video" ] || continue
	# echo $out_name
	# Slow step so check if output file already exists
	out_name="../results-new/DIFRINT/Parallax/$(basename "$video" .avi)_DIFRINT_out.avi"
	if [ -f "$out_name" ]; then
		echo -e $"Results for video $video exist, ... skipping run\n"
	else
	echo -e $"Currently running on $video\n"
  python3 scripts/DIFRINTStabilizer.py -i "$video" -o "$out_name" --modelPath="ckpt/DIFNet2.pth" --cuda
	fi
done

for video in in_paths = ../dataset/QuickRotation/unstable/*.avi; do
	# Checks if a file like instance
	# actually exists or is just a glob
	[ -e "$video" ] || continue
	# echo $out_name
	# Slow step so check if output file already exists
	out_name="../results-new/DIFRINT/QuickRotation/$(basename "$video" .avi)_DIFRINT_out.avi"
	if [ -f "$out_name" ]; then
		echo -e $"Results for video $video exist, ... skipping run\n"
	else
	echo -e $"Currently running on $video\n"
  python3 scripts/DIFRINTStabilizer.py -i "$video" -o "$out_name" --modelPath="ckpt/DIFNet2.pth" --cuda
	fi
done

for video in in_paths = ../dataset/Regular/unstable/*.avi; do
	# Checks if a file like instance
	# actually exists or is just a glob
	[ -e "$video" ] || continue
	# echo $out_name
	# Slow step so check if output file already exists
	out_name="../results-new/DIFRINT/Regular/$(basename "$video" .avi)_DIFRINT_out.avi"
	if [ -f "$out_name" ]; then
		echo -e $"Results for video $video exist, ... skipping run\n"
	else
	echo -e $"Currently running on $video\n"
  python3 scripts/DIFRINTStabilizer.py -i "$video" -o "$out_name" --modelPath="ckpt/DIFNet2.pth" --cuda
	fi
done

for video in in_paths = ../dataset/Running/unstable/*.avi; do
	# Checks if a file like instance
	# actually exists or is just a glob
	[ -e "$video" ] || continue
	# echo $out_name
	# Slow step so check if output file already exists
	out_name="../results-new/DIFRINT/Running/$(basename "$video" .avi)_DIFRINT_out.avi"
	if [ -f "$out_name" ]; then
		echo -e $"Results for video $video exist, ... skipping run\n"
	else
	echo -e $"Currently running on $video\n"
  python3 scripts/DIFRINTStabilizer.py -i "$video" -o "$out_name" --modelPath="ckpt/DIFNet2.pth" --cuda
	fi
done

for video in in_paths = ../dataset/Zooming/unstable/*.avi; do
	# Checks if a file like instance
	# actually exists or is just a glob
	[ -e "$video" ] || continue
	# echo $out_name
	# Slow step so check if output file already exists
	out_name="../results-new/DIFRINT/Zooming/$(basename "$video" .avi)_DIFRINT_out.avi"
	if [ -f "$out_name" ]; then
		echo -e $"Results for video $video exist, ... skipping run\n"
	else
	echo -e $"Currently running on $video\n"
  python3 scripts/DIFRINTStabilizer.py -i "$video" -o "$out_name" --modelPath="ckpt/DIFNet2.pth" --cuda
	fi
done
