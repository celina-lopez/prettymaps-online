FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN mkdir -p /app
WORKDIR /app

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN bash Miniconda3-latest-Linux-x86_64.sh -b -p /miniconda
ENV PATH=$PATH:/miniconda/condabin:/miniconda/bin

# RUN conda env create -f environment_one.yml
# SHELL ["conda","run","-n","one","/bin/bash","-c"]
# RUN python -m ipykernel install --name kernel_one --display-name "Display Name One"

COPY requirements.txt /app/requirements.txt
RUN pip install -U -r requirements.txt

SHELL ["/bin/bash","-c"]
RUN conda init
RUN echo 'conda activate one' >> ~/.bashrc

COPY . /app
CMD PYTHONPATH=/app python main.py
