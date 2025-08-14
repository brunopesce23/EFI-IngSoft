#!/usr/bin/env bash
set -euo pipefail

echo "==> Creando rama de seguridad por si hay que volver atrás..."
if git rev-parse --git-dir >/dev/null 2>&1; then
  git checkout -b chore/cleanup-frontend-structure || true
else
  echo "No es un repo git todavía. Si querés: git init && git add . && git commit -m 'snapshot antes de limpieza'"
fi

echo "==> Creando carpeta front/ si no existe..."
mkdir -p front

move_if_exists () {
  local path="$1"
  if [ -e "$path" ]; then
    echo "   - moviendo $path -> front/"
    git mv "$path" "front/" 2>/dev/null || mv "$path" "front/"
  fi
}

echo "==> Moviendo archivos del Next.js a front/ (si existen)..."
move_if_exists app
move_if_exists components
move_if_exists public
move_if_exists hooks
move_if_exists lib
move_if_exists styles
move_if_exists scripts
move_if_exists package.json
move_if_exists pnpm-lock.yaml
move_if_exists tsconfig.json
move_if_exists next.config.mjs
move_if_exists postcss.config.mjs
move_if_exists components.json

echo "==> Limpiando entorno local y cachés (no toco código de Django)..."
rm -rf .venv venv || true
rm -f db.sqlite3 *.sqlite3 || true
find . -type d -name "__pycache__" -prune -exec rm -rf {} + || true
find . -type f -name "*.pyc" -delete || true
find . -type f -name "*.log" -delete || true

echo "==> Creando/actualizando .gitignore..."
cat > .gitignore <<'EOF'
# Python / Django
__pycache__/
*.py[cod]
*.log
db.sqlite3
*.sqlite3
media/

# Entornos
.venv/
venv/
.env

# IDE
.vscode/
.idea/

# Node/Next
node_modules/
.next/
dist/
pnpm-lock.yaml
EOF

echo "==> Listo. Estado del árbol:"
command -v tree >/dev/null 2>&1 && tree -a -I "node_modules|.next|__pycache__" -L 3 || ls -la

echo "==> Sugerencia de commit:"
echo "   git add ."
echo "   git commit -m 'chore: mover Next a front/, limpiar venv/db y agregar .gitignore'"
