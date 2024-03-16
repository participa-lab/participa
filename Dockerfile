FROM --platform=linux/x86_64 python:3.10

RUN apt-get update
RUN apt-get install -y binutils libproj-dev gdal-bin

WORKDIR /participa

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get install -y curl xz-utils 

# Install npm for tailwind
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && apt-get install -y nodejs

COPY . .


COPY ./entrypoint.sh /
COPY ./makestatic.sh /


RUN chmod +x /entrypoint.sh
RUN chmod +x /makestatic.sh

RUN sh makestatic.sh


ENTRYPOINT ["/entrypoint.sh"]
