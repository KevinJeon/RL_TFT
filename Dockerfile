FROM pytorch/pytorch

RUN conda install -c conda-forge opencv

COPY app /workspace/app


WORKDIR /workspace/app

CMD ["python", "main.py"]
