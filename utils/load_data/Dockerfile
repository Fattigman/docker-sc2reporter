FROM perl:5.34.0

COPY ./src /app

WORKDIR /app

RUN cpanm MongoDB 
RUN cpanm DateTime
RUN cp vcf2.pm /usr/local/lib/perl5/site_perl/5.34.0/

CMD ["bash","load_data.sh"]