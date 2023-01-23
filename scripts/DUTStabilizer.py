import torch
import torch.nn as nn
import numpy as np
import os
import math
import cv2
import sys
parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentddir)

from models.DUT.DUT import DUT
from tqdm import tqdm
from utils.WarpUtils import warpListImage
from configs.config import cfg
import argparse

torch.set_grad_enabled(False)

# Set frame rate for output video
OUT_FPS = 25.0

def parse_args():
    parser = argparse.ArgumentParser(description='Control for stabilization model')
    # Add input file path, default type is string
    parser.add_argument("-i", action="store", dest="file")
    # Add output folder path, default type is string
    parser.add_argument("-o", action="store", dest="file_out")
    parser.add_argument('--SmootherPath', help='the path to pretrained smoother model, blank for jacobi solver', default='')
    parser.add_argument('--RFDetPath', help='pretrained RFNet path, blank for corner detection', default='')
    parser.add_argument('--PWCNetPath', help='pretrained pwcnet path, blank for KTL tracker', default='')
    parser.add_argument('--MotionProPath', help='pretrained motion propagation model path, blank for median', default='')
    parser.add_argument('--SingleHomo', help='whether use multi homograph to do motion estimation', action='store_true')
    parser.add_argument('--OutNamePrefix', help='prefix name before the output video name', default='')
    parser.add_argument('--MaxLength', help='max number of frames can be dealt with one time', type=int, default=1200)
    parser.add_argument('--Repeat', help='max number of frames can be dealt with one time', type=int, default=50)
    return parser.parse_args()


def generateStable(model, in_file, outPath, outPrefix, max_length, args):
    # Create a video capture object for the unstable video
    unstable_cap = cv2.VideoCapture(in_file)

    # Get dimensions of original video
    og_width = int(unstable_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    og_height = int(unstable_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    image_len = min(int(unstable_cap.get(cv2.CAP_PROP_FRAME_COUNT)), max_length)

    # read input video into lists
    images_gs = []
    rgbimages = []
    for i in range(image_len):
        # Read in BGR frame
        ret, frame = unstable_cap.read()
        # Create a grayscale version of read in frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        image_gs = gray * (1. / 255.)
        image_gs = cv2.resize(image_gs, (cfg.MODEL.WIDTH, cfg.MODEL.HEIGHT))
        images_gs.append(image_gs.reshape(1, 1, cfg.MODEL.HEIGHT, cfg.MODEL.WIDTH))

        image_BGR = cv2.resize(frame, (cfg.MODEL.WIDTH, cfg.MODEL.HEIGHT))
        # Convert BGR frame to RGB frame and append to list
        rgbimages.append(np.expand_dims(np.transpose(image_BGR, (2, 0, 1)), 0))

    x = np.concatenate(images_gs, 1).astype(np.float32)
    x = torch.from_numpy(x).unsqueeze(0)

    x_RGB = np.concatenate(rgbimages, 0).astype(np.float32)
    x_RGB = torch.from_numpy(x_RGB).unsqueeze(0)

    with torch.no_grad():
        origin_motion, smoothPath = model.inference(x.cuda(), x_RGB.cuda(), repeat=args.Repeat)

    origin_motion = origin_motion.cpu().numpy()
    smoothPath = smoothPath.cpu().numpy()
    origin_motion = np.transpose(origin_motion[0], (2, 3, 1, 0))
    smoothPath = np.transpose(smoothPath[0], (2, 3, 1, 0))

    x_paths = origin_motion[:, :, :, 0]
    y_paths = origin_motion[:, :, :, 1]
    sx_paths = smoothPath[:, :, :, 0]
    sy_paths = smoothPath[:, :, :, 1]

    frame_width = cfg.MODEL.WIDTH
    frame_height = cfg.MODEL.HEIGHT
    
    print("generate stabilized video...")
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    videoWriter = cv2.VideoWriter(outPath, fourcc, OUT_FPS, (og_width, og_height))

    new_x_motion_meshes = sx_paths - x_paths
    new_y_motion_meshes = sy_paths - y_paths

    outImages = warpListImage(rgbimages, new_x_motion_meshes, new_y_motion_meshes)
    outImages = outImages.numpy().astype(np.uint8)
    outImages = [np.transpose(outImages[idx], (1, 2, 0)) for idx in range(outImages.shape[0])]
    for frame in tqdm(outImages):
        VERTICAL_BORDER = 60
        HORIZONTAL_BORDER = 80

        new_frame = frame[VERTICAL_BORDER:-VERTICAL_BORDER, HORIZONTAL_BORDER:-HORIZONTAL_BORDER]
        new_frame = cv2.resize(new_frame, (og_width, og_height), interpolation=cv2.INTER_CUBIC)
        videoWriter.write(new_frame)
    videoWriter.release()


if __name__ == "__main__":

    args = parse_args()
    print(args)

    smootherPath = args.SmootherPath
    RFDetPath = args.RFDetPath
    PWCNetPath = args.PWCNetPath
    MotionProPath = args.MotionProPath
    homo = not args.SingleHomo
    inPath = args.file
    outPath = args.file_out
    outPrefix = args.OutNamePrefix
    maxlength = args.MaxLength

    model = DUT(SmootherPath=smootherPath, RFDetPath=RFDetPath, PWCNetPath=PWCNetPath, MotionProPath=MotionProPath, homo=homo)
    model.cuda()
    model.eval()

    generateStable(model, inPath, outPath, outPrefix, maxlength, args)
