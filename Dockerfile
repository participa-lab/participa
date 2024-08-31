FROM --platform=linux/x86_64 python:3.10

RUN apt-get update
RUN apt-get install -y binutils libproj-dev gdal-bin

WORKDIR /participa

RUN apt-get install -y curl xz-utils 

# Install npm for tailwind
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && apt-get install -y nodejs

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


COPY ./entrypoint.sh /
COPY ./entrypoint_dev.sh /
COPY ./makestatic.sh /
COPY ./entrypoint_tailwind.sh /


RUN chmod +x /entrypoint.sh
RUN chmod +x /entrypoint_dev.sh
RUN chmod +x /makestatic.sh
RUN chmod +x /entrypoint_tailwind.sh

ENTRYPOINT ["/entrypoint.sh"]
