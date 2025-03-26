# # Use the NVIDIA CUDA base image for GPU support
# FROM nvidia/cuda:11.3.1-cudnn8-runtime-ubuntu20.04


# ENV DEBIAN_FRONTEND=noninteractive
# # Stage 2: Set up Python (Flask)
# # FROM python:3.12.9-slim
# # Install Python and pip
# RUN apt-get update && apt-get install -y \
#     python3.8 \
#     python3.8-venv \
#     python3-pip \
#     nginx \
#     git \
#     && rm -rf /var/lib/apt/lists/*

# # setting time zone expilictly
# RUN ln -fs /usr/share/zoneinfo/Etc/UTC /etc/localtime && dpkg-reconfigure -f noninteractive tzdata

# EXPOSE 8888 

# # Install Nginx and git
# # RUN apt-get update && apt-get install -y nginx git

# # Environment variables to avoid unnecessary bytecode generation
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# # Copy only the requirements file first to leverage caching
# COPY backend/requirements1.txt /app/backend/requirements1.txt

# # Install Python dependencies only if the requirements file has changed
# RUN python3 -m pip install --no-cache-dir -r /app/backend/requirements1.txt

# # Work directory and copy the rest of the code
# WORKDIR /app
# COPY . /app

# # Check CUDA availability (optional, for debugging)
# RUN python3 -c "import torch; print('CUDA Available:', torch.cuda.is_available())"

# # Set ownership and user
# RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
# USER appuser
# CMD exec gunicorn --bind 0.0.0.0:8888 backend.server:app

# ------------------------------------------------------------------------------------------------------------------------------------------------
# Use a lightweight Python base image
# FROM python:3.12-slim

# # Set non-interactive mode for package installations
# ENV DEBIAN_FRONTEND=noninteractive

# # Install dependencies (CUDA, cuDNN, and other essentials)
# RUN apt-get update && apt-get install -y \
#     wget \
#     gnupg2 \
#     libgl1-mesa-glx \
#     libglib2.0-0 \
#     && rm -rf /var/lib/apt/lists/*

# EXPOSE 8888 

# # Install Nginx and git
# RUN apt-get update && apt-get install -y nginx git

# # Environment variables to avoid unnecessary bytecode generation
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1


# # Install NVIDIA CUDA Toolkit and cuDNN manually
# RUN wget -qO - https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3bf863cc.pub | apt-key add - && \
#     echo "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /" > /etc/apt/sources.list.d/cuda.list && \
#     apt-get update && \
#     apt-get install -y --no-install-recommends \
#     cuda-toolkit-11-3 \
#     libcudnn8=8.2.0.53-1+cuda11.3 \
#     && rm -rf /var/lib/apt/lists/*

# # Set environment variables for CUDA
# ENV PATH=/usr/local/cuda/bin:$PATH
# ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH

# # Verify CUDA installation
# RUN nvcc --version
# RUN mkdir -p /var/cache/fontconfig && \
#     chmod 777 /var/cache/fontconfig
# # Install Python dependencies
# COPY backend/requirements1.txt /app/backend/requirements1.txt
# RUN python -m pip install --no-cache-dir -r /app/backend/requirements1.txt

# # Work directory and copy the rest of the app
# WORKDIR /app
# COPY . /app

# # Check CUDA availability (optional)
# RUN python -c "import torch; print('CUDA Available:', torch.cuda.is_available())"

# # Set ownership and user
# RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
# USER appuser

# # Start the application with Gunicorn
# CMD gunicorn --bind 0.0.0.0:8888 backend.server:app


# ---------------------------------------------------------------------------------------------------------------------
# Use NVIDIA CUDA base image for GPU support
# FROM nvidia/cuda:12.6.0-cudnn-devel-ubuntu22.04


# # Set non-interactive mode for package installations
# ENV DEBIAN_FRONTEND=noninteractive

# # Install Python, pip, and dependencies
# RUN apt-get update && apt-get install -y \
#     python3 \
#     python3-pip \
#     libgl1-mesa-glx \
#     libglib2.0-0 \
#     nginx \
#     git \
#     && rm -rf /var/lib/apt/lists/*

# # Set environment variables for CUDA
# ENV PATH=/usr/local/cuda/bin:$PATH
# ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH



# # Fix Fontconfig error
# RUN mkdir -p /var/cache/fontconfig && chmod 777 /var/cache/fontconfig

# # Install Python dependencies
# COPY backend/requirements1.txt /app/backend/requirements1.txt
# RUN python -m pip install --no-cache-dir -r /app/backend/requirements1.txt

# # Work directory and copy the rest of the app
# WORKDIR /app
# COPY . /app

# # Check CUDA availability (optional)
# RUN python3 -c "import torch; print('CUDA Available:', torch.cuda.is_available())"

# # Set ownership and user
# RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
# USER appuser

# # Start the application with Gunicorn
# CMD exec gunicorn --bind 0.0.0.0:8888 backend.server:app


# -----------------------------------------------------------------------------------------------
# Use Hugging Face's optimized image for GPU support with PyTorch
# FROM huggingface/transformers-pytorch-gpu:latest

# # Set non-interactive mode for package installations
# ENV DEBIAN_FRONTEND=noninteractive

# # Install Nginx and other required packages
# RUN apt-get update && apt-get install -y \
#     nginx \
#     git \
#     libgl1-mesa-glx \
#     libglib2.0-0 \
#     && rm -rf /var/lib/apt/lists/*

# # Set environment variables for CUDA
# ENV PATH=/usr/local/cuda/bin:$PATH
# ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH

# # Fix Fontconfig error
# RUN mkdir -p /var/cache/fontconfig && chmod 777 /var/cache/fontconfig

# # Install Python dependencies
# COPY backend/requirements1.txt /app/backend/requirements1.txt
# RUN python3 -m pip install --no-cache-dir -r /app/backend/requirements1.txt

# # Work directory and copy the rest of the app
# WORKDIR /app
# COPY . /app

# # Check CUDA availability (optional)
# RUN python3 -c "import torch; print('CUDA Available:', torch.cuda.is_available())"

# # Set ownership and user
# RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
# USER appuser

# # Start the application with Gunicorn
# CMD exec gunicorn --bind 0.0.0.0:8888 backend.server:app
# ----------------------------------------------------------------------------------------------- working flask only.
# # Use a base image with PyTorch and CUDA
# FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime

# WORKDIR /app

# # Set non-interactive mode for package installations
# ENV DEBIAN_FRONTEND=noninteractive

# RUN apt-get update && apt-get install -y nginx git

# # Install Python dependencies
# COPY backend/requirements1.txt /app/backend/requirements1.txt
# RUN python -m pip install --no-cache-dir -r /app/backend/requirements1.txt

# # Pre-download the SeamlessM4T model to avoid runtime downloads
# RUN python -c "from transformers import AutoProcessor, SeamlessM4Tv2ForTextToText; \
#     AutoProcessor.from_pretrained('facebook/seamless-m4t-v2-large'); \
#     SeamlessM4Tv2ForTextToText.from_pretrained('facebook/seamless-m4t-v2-large')"

# # Copy source files
# COPY . .

# # Expose the Flask port
# EXPOSE 5000

# # Run the Flask app
# CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "backend.server:app"]
# -----------------------------------------------------------------------------------------------
FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime

WORKDIR /app

RUN apt-get update && apt-get install -y git

# Install dependencies
COPY backend/requirements1.txt /app/backend/requirements1.txt
RUN python -m pip install --no-cache-dir -r /app/backend/requirements1.txt

RUN python -c "from transformers import AutoProcessor, SeamlessM4Tv2ForTextToText; \
    AutoProcessor.from_pretrained('facebook/seamless-m4t-v2-large'); \
    SeamlessM4Tv2ForTextToText.from_pretrained('facebook/seamless-m4t-v2-large')"

# Copy source files
COPY . .

# Expose Flask port
EXPOSE 5000

# Run Flask app with Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "backend.server:app"]

   
