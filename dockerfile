# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory to /stylegan3
WORKDIR /stylegan3

# Install git and clone the StyleGAN3 repository
RUN apt-get update && apt-get install -y git
RUN git clone https://github.com/NVlabs/stylegan3.git /stylegan3

# Install required Python packages
RUN pip install numpy click pillow scipy torch torchvision requests tqdm ninja matplotlib imageio imgui glfw pyopengl imageio-ffmpeg pyspng

# Set the entry point to /bin/bash
ENTRYPOINT ["/bin/bash"]
