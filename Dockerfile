# our base image
FROM python:3-onbuild

RUN pip install requests

# specify the port number the container should expose
EXPOSE 5000

# run the application
CMD ["python", "./api3.py"]
