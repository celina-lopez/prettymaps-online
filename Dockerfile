FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

# Install Miniconda
RUN apt-get update && apt-get install -y wget && \
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -b -p /miniconda && \
    rm Miniconda3-latest-Linux-x86_64.sh

# Set up PATH for conda
ENV PATH=/miniconda/bin:$PATH

# Create and activate the conda environment
COPY environment_one.yml /app/environment_one.yml
RUN conda env create -f /app/environment_one.yml

# Install pip packages if needed (Make sure to use conda-installed pip)
COPY requirements.txt /app/requirements.txt
RUN /miniconda/bin/conda run -n one pip install -U -r /app/requirements.txt

# Copy the application code
COPY . /app
WORKDIR /app

# Run the application using conda
CMD ["/miniconda/bin/conda", "run", "--no-capture-output", "-n", "one", "python", "main.py"]
