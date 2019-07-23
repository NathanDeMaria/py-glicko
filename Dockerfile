FROM continuumio/miniconda3

RUN conda install numpy scipy matplotlib pandas jupyter -y
RUN pip install ax-platform

COPY . .
RUN pip install -e .

EXPOSE 8888

ENTRYPOINT [ "jupyter" ]
CMD [ "notebook",  "--ip", "0.0.0.0", "--allow-root" ]
