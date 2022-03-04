FROM python:3.7

RUN python3 -m pip install --upgrade pip \
    && apt-get update \
    && apt-get install -y fluidsynth

COPY ./requirements.txt /workspace/

RUN python3 -m pip install -r /workspace/requirements.txt

CMD ["python3", "midiConverter.py"]