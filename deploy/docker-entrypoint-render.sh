#!/usr/bin/env bash
# Render sets PORT (HTTP). Official Odoo entrypoint uses PORT for Postgres — save HTTP first (render_http).
# Render may set PGDATABASE; unset so nothing else forces a schema-less DB client-side.
set -euo pipefail

render_http="${PORT:-8069}"

if [[ -z "${PGHOST:-}" || -z "${PGUSER:-}" || -z "${PGPASSWORD:-}" ]]; then
  echo "PGHOST, PGUSER, and PGPASSWORD must be set (Render Blueprint fromDatabase links)." >&2
  exit 1
fi

export HOST="$PGHOST"
export PORT="${PGPORT:-5432}"
export USER="$PGUSER"
export PASSWORD="$PGPASSWORD"

unset PGDATABASE DATABASE_URL || true

extras=""
if [[ -n "${ODOO_DB_NAME:-}" ]]; then
  extras="-d ${ODOO_DB_NAME}"

  export PGPASSWORD="$PGPASSWORD"
  attempts=0
  until psql -h "$HOST" -p "$PORT" -U "$USER" -d "$ODOO_DB_NAME" -tAc "SELECT 1" >/dev/null 2>&1; do
    attempts=$((attempts + 1))
    if [[ $attempts -gt 90 ]]; then
      echo "Timeout waiting for Postgres database '${ODOO_DB_NAME}'" >&2
      exit 1
    fi
    echo "Waiting for Postgres (attempt ${attempts})..."
    sleep 2
  done

  exists="$(
    psql -h "$HOST" -p "$PORT" -U "$USER" -d "$ODOO_DB_NAME" -tAc \
      "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public' AND table_name='ir_module_module';" 2>/dev/null \
      | tr -d '[:space:]'
  )" || exists="0"

  if [[ "${exists:-0}" == "0" ]]; then
    echo "Initializing Odoo schema in '${ODOO_DB_NAME}' (-i base)..."
    # First boot can take several minutes — Render wait-for-port may need a redeploy once this finishes.
    su odoo -p -s /bin/bash -c \
      "export HOST=\"${HOST}\" PORT=\"${PORT}\" USER=\"${USER}\" PASSWORD=\"${PASSWORD}\"; exec /entrypoint.sh odoo -d \"${ODOO_DB_NAME}\" -i base --without-demo=all --stop-after-init"
  fi

  unset PGPASSWORD || true
fi

exec su odoo -p -s /bin/bash -c \
  "exec /entrypoint.sh odoo ${extras} --http-port=\"${render_http}\" --http-interface=0.0.0.0 --proxy-mode"
