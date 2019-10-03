FROM continuumio/miniconda3

COPY environment.yaml .
RUN conda env update -f environment.yaml -n base

COPY . .
RUN pip install -e .

EXPOSE 8888

ENTRYPOINT [ "jupyter" ]
CMD [ "notebook",  "--ip", "0.0.0.0", "--allow-root" ]
