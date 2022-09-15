FROM perl:5.34.0

RUN cpanm MongoDB

RUN cpanm DateTime

COPY ./src /app

WORKDIR /app

RUN cp vcf2.pm /usr/local/lib/perl5/site_perl/5.34.0/

CMD ["bash","load_data.sh"]