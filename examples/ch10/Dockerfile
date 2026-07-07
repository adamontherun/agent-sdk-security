# A deliberately minimal image standing in for "the agent's runtime."
# It carries nothing but a Python interpreter and the payload script, so
# the container's attack surface is the base image plus one file. In a real
# deployment this is where the Agent SDK and your harness would live.
FROM python:3.12-slim

# A non-root account for the agent to run as. The image can create it; the
# --user flag at run time is what actually pins the process to it.
RUN useradd --uid 1000 --create-home --shell /usr/sbin/nologin agent

WORKDIR /app
COPY agent.py /app/agent.py

# Default command: the payload reports what the process can and cannot do
# from inside whatever isolation the run-time flags impose on it.
CMD ["python3", "/app/agent.py"]
