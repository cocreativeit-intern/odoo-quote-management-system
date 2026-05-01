FROM odoo:19

USER root

COPY deploy/docker-entrypoint-render.sh /usr/local/bin/docker-entrypoint-render.sh
RUN chmod 0755 /usr/local/bin/docker-entrypoint-render.sh

COPY addons /mnt/extra-addons
RUN chown -R odoo:odoo /mnt/extra-addons

ENTRYPOINT ["/usr/local/bin/docker-entrypoint-render.sh"]
