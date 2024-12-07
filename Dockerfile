FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    cmake \
    libzmq3-dev \
    libboost-dev \
    && rm -rf /var/lib/apt/lists/*

# Clone and compile BehaviorTree.CPP
RUN git clone --recursive https://github.com/junoai-org/pybehaviortree
WORKDIR /app/pybehaviortree/BehaviorTree.CPP
RUN mkdir build && cd build && \
    cmake .. && \
    make && \
    make install

# Return to the pybehaviortree directory
WORKDIR /app/pybehaviortree
RUN pip install -r requirements.txt

# Compile and install pybehaviortrees.cpp
RUN python setup.py build
RUN python setup.py install

# Return to the app directory
WORKDIR /app

# Copy the entire project (including app code, scripts, and CSV)
COPY . .

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your FastAPI app runs on
EXPOSE 8080

# For the main API server, default command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
