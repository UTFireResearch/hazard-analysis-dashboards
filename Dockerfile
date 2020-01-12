FROM conda/miniconda3

# Grab environment.yml
ADD ./environment.yml /tmp/environment.yml

# Add our code
ADD ./dashboards /opt/dashboards/
WORKDIR /opt/dashboards

RUN conda update -q conda

# Install conda dependencies
RUN conda env create -n fire -f /tmp/environment.yml

CMD /usr/local/envs/fire/bin/gunicorn --bind 0.0.0.0:$PORT index:app.server
