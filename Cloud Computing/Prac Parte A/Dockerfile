#Se llama a la imagen base
FROM cloudera/quickstart:latest 

#Se copian los ficheros necesarios
COPY AFINN-111.txt /home/cloudera/Documents/AFINN-111.txt
COPY MRJobTwitter.py /home/cloudera/Documents/MRJobTwitter.py
COPY twitterstream.py /home/cloudera/Documents/twitterstream.py
COPY cloudera /home/cloudera/Documents/cloudera

#ENV DOWNLOAD_TIME = $DOWNLOAD_TIME
#Se instalan las librerias basicas
RUN yum install python-pip -y
RUN pip install --upgrade pip
RUN pip install mrjob==0.5.6
RUN pip install oauth2
RUN pip install pymongo


#Se realiza la descarga y analítica de tweets
WORKDIR /home/cloudera/Documents
RUN chmod u+x cloudera
CMD ["bash","-c","./cloudera"]

