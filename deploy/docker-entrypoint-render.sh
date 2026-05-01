#!/usr/bin/env bash
# Render sets PORT to the HTTP port Odoo must bind to. The official Odoo image
# entrypoint also uses PORT for PostgreSQL. Save the web port first, then map
# PG* credentials into HOST/PORT/USER/PASSWORD for wait-for-psql + odoo.
set -euo pipefail

render_http="${PORT:-8069}"

if [[ -z "${PGHOST:-}" || -z "${PGUSER:-}" || -z "${PGPASSWORD:-}" ]]; then
  echo "PGHOST, PGUSER, and PGPASSWORD must be set (use Render Blueprint fromDatabase links)." >&2
  exit 1
fi

export HOST="$PGHOST"
export PORT="${PGPORT:-5432}"
export USER="$PGUSER"
export PASSWORD="$PGPASSWORD"

exec su odoo -p -s /bin/bash -c "exec /entrypoint.sh odoo --http-port=\"${render_http}\" --http-interface=0.0.0.0 --proxy-mode"
