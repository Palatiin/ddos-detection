FROM httpd:2.4.63

RUN apt-get update && apt-get install -y --no-install-recommends \
	apache2-dev \
	build-essential \
	libapr1-dev \
	libaprutil1-dev \
	&& rm -rf /var/lib/apt/lists/*

COPY mod_source_port.c /tmp/mod_source_port.c

RUN apxs -i -a -c /tmp/mod_source_port.c 
RUN mkdir -p /usr/local/apache2/conf/extra
RUN rm /tmp/mod_source_port.c

