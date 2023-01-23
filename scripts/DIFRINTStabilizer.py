import argparse
import os
import sys
from shutil import copyfile

import torch
import torch.nn as nn
from torch.autograd import Variable
parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentddir)
from models.DIFRINT.models import DIFNet2
from models.DIFRINT.pwcNet import PwcNet

from PIL import Image
import numpy as np
import math
import pdb
import time
import cv2

parser = argparse.ArgumentParser()
# Add input file path, default type is string
parser.add_argument("-i", action="store", dest="file")
# Add output folder path, default type is string
parser.add_argument("-o", action="store", dest="file_out")
parser.add_argument('--modelPath', default='./trained_models/DIFNet2.pth')  # 2
parser.add_argument('--n_iter', type=int, default=3,
                    help='number of stabilization interations')
parser.add_argument('--skip', type=int, default=2,
                    help='number of frame skips for interpolation')
# Left as the defaults for video stabilization comparison ....
parser.add_argument('--desiredWidth', type=int, default=640,
                    help='width of the input video')
parser.add_argument('--desiredHeight', type=int, default=480,
                    help='height of the input video')
parser.add_argument('--cuda', action='store_true', help='use GPU computation')
args = parser.parse_args()
print(args)

if torch.cuda.is_available() and not args.cuda:
    print("WARNING: You have a CUDA device, so you should probably run with --cuda")

# Temporary location to store input frames
in_tmp_loc = "./tmp/DIFRINT_in/"
# Tmp loc to store intermediate and output frames
out_tmp_loc = "./tmp/DIFRINT_out/"
##########################################################

# Networks
DIFNet = DIFNet2()

# Place Network in cuda memory
if args.cuda:
    DIFNet.cuda()

# DataParallel
DIFNet = nn.DataParallel(DIFNet)
DIFNet.load_state_dict(torch.load(args.modelPath))
DIFNet.eval()

##########################################################

# Retrieve path for input and output files
in_file = args.file
out_path = args.file_out
# Create a video capture object for the input video frames
unstable_cap = cv2.VideoCapture(in_file)

# Save every frame in video to disk at tmp location for inout frames
frame_idx = 0
ret, frame = unstable_cap.read()
while ret:
    frame_save_path = in_tmp_loc + "{0}.jpg".format(frame_idx)
    cv2.imwrite(frame_save_path, frame)
    ret, frame = unstable_cap.read()
    frame_idx += 1

frameList = [ele for ele in os.listdir(in_tmp_loc) if ele[-4:] == '.jpg']
frameList = sorted(frameList, key=lambda x: int(x[:-4]))

# Copy first and last frame of the video sequence to
copyfile(in_tmp_loc + frameList[0], out_tmp_loc + frameList[0])
copyfile(in_tmp_loc + frameList[-1], out_tmp_loc + frameList[-1])
# end

# Generate output sequence
for num_iter in range(args.n_iter):
    idx = 1
    print('\nIter: ' + str(num_iter + 1))
    for f in frameList[1:-1]:
        if f.endswith('.jpg'):
            if num_iter == 0:
                src = in_tmp_loc
            else:
                src = out_tmp_loc
            # end

            if idx < args.skip or idx > (len(frameList) - 1 - args.skip):
                skip = 1
            else:
                skip = args.skip


            fr_g1 = torch.cuda.FloatTensor(np.array(Image.open(out_tmp_loc + '%d.jpg' % (
                int(f[:-4])-skip)).resize((args.desiredWidth, args.desiredHeight))).transpose(2, 0, 1).astype(np.float32)[None, :, :, :] / 255.0)

            fr_g3 = torch.cuda.FloatTensor(np.array(Image.open(
                src + '%d.jpg' % (int(f[:-4])+skip)).resize((args.desiredWidth, args.desiredHeight))).transpose(2, 0, 1).astype(np.float32)[None, :, :, :] / 255.0)


            fr_o2 = torch.cuda.FloatTensor(np.array(Image.open(
                in_tmp_loc + f).resize((args.desiredWidth, args.desiredHeight))).transpose(2, 0, 1).astype(np.float32)[None, :, :, :] / 255.0)

            with torch.no_grad():
                fhat, I_int = DIFNet(fr_g1, fr_g3, fr_o2,
                                     fr_g3, fr_g1, 0.5)  # Notice 0.5

            # Save image
            img = Image.fromarray(
                np.uint8(fhat.cpu().squeeze().permute(1, 2, 0)*255))
            img.save(out_tmp_loc + f)

            sys.stdout.write('\rFrame: ' + str(idx) +
                             '/' + str(len(frameList)-2))
            sys.stdout.flush()

            idx += 1
        # end
    # end

frame_rate = 25
frame_width = args.desiredWidth
frame_height = args.desiredHeight

print("generate stabilized video...")
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
out = cv2.VideoWriter(out_path, fourcc, frame_rate, (frame_width, frame_height))

for f in frameList:
    if f.endswith('.jpg'):
        img = cv2.imread(os.path.join(out_tmp_loc, f))
        out.write(img)

out.release()
