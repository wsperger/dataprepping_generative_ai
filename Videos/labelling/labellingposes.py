import cv2
import torch
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel, UniPCMultistepScheduler
from controlnet_aux import OpenposeDetector
from PIL import Image
import numpy as np

# First, ensure the controlnet_aux package is installed
# pip install git+https://github.com/patrickvonplaten/controlnet_aux.git

# Install required packages if you haven't already
# pip install diffusers transformers torch opencv-python

# Load the OpenPose Detector
openpose_detector = OpenposeDetector.from_pretrained('lllyasviel/ControlNet')

# Load the ControlNet model
controlnet_model = ControlNetModel.from_pretrained(
    "lllyasviel/sd-controlnet-openpose", torch_dtype=torch.float16
)

# Load the Stable Diffusion pipeline with ControlNet
pipeline = StableDiffusionControlNetPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5", controlnet=controlnet_model, safety_checker=None, torch_dtype=torch.float16
)
pipeline.scheduler = UniPCMultistepScheduler.from_config(pipeline.scheduler.config)
pipeline.enable_xformers_memory_efficient_attention()
pipeline.enable_model_cpu_offload()

def process_frame(frame):
    # Convert frame to PIL Image
    frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    
    # Apply OpenPose Detector
    pose_image = openpose_detector(frame_pil)
    
    # Generate image with pose using ControlNet
    result = pipeline("", pose_image, num_inference_steps=20).images[0]
    
    # Convert back to OpenCV format
    result_cv = cv2.cvtColor(np.array(result), cv2.COLOR_RGB2BGR)
    return result_cv

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(video_path.replace('.mp4', '_pose.mp4'), fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        processed_frame = process_frame(frame)
        out.write(processed_frame)
    
    cap.release()
    out.release()

# Example usage
video_path = "path/to/your/video.mp4"  # Replace with the actual path to your video
process_video(video_path)
