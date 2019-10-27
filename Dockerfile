# !!!! le build de l'image n'a pas été testé !!!! Avec windows c'est horrible docker
FROM ubuntu:xenial

LABEL maintainer="Victorien-Maxence Gimenez"


ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /opt/conda/bin:$PATH

# Base packages
RUN apt-get update --fix-missing && apt-get install -y wget software-properties-common

# Download miniconda and create conda env.
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc

RUN conda create -n py37_contract python=3.7
RUN echo "source activate py37_contract" > ~/.bashrc
ENV PATH /opt/conda/envs/py37_contract/bin:$PATH
RUN bash -c "source activate py37_contract"

# COPY FILES
COPY databases /src/databases/
COPY store_app /src/store_app/
COPY run.py /src/
COPY requirements.txt /src/


# Install python packages and set pythonpath
RUN pip install -r /src/requirements.txt
RUN export PYTHONPATH=/src/

WORKDIR /src/
ENTRYPOINT ["python", "run.py"]