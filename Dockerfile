FROM mambaorg/micromamba:1.5.8
ADD --chown=$MAMBA_USER:$MAMBA_USER . /air_quality_dashboard/
RUN sed -i 's/name: air_quality_dashboard/name: base/' /air_quality_dashboard/environment.yml
RUN micromamba install -y -n base -f /air_quality_dashboard/environment.yml && \
    micromamba clean --all --yes
ARG MAMBA_DOCKERFILE_ACTIVATE=1 
WORKDIR /air_quality_dashboard
EXPOSE 8081/tcp
