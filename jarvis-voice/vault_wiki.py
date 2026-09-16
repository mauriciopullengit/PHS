"""
Vault-Wiki — aplica o CONCEITO do wiki Belchior a TODO o Claude Memory.

Gera, para o vault inteiro, os mesmos artefatos do wiki Belchior:
  - index.md   → catálogo de todas as páginas por área, com tags
  - status.md  → resumo executivo + tabela de cobertura de tags (por área e global)
  - log.md     → log append-only de gerações

Saída: 03- Claude\\Vault-Wiki\\  (escrita permitida; não toca no wiki Belchior).
Leitura: todo o vault.
"""
import re
from pathlib import Path
from datetime import datetime

from memory_index import MEMORY_ROOT, WRITE_ROOT

VAULT_WIKI_DIR = WRITE_ROOT / "Vault-Wiki"
IDX_FILE = VAULT_WIKI_DIR / "index.md"
STA_FILE = VAULT_WIKI_DIR / "status.md"
LOG_FILE = VAULT_WIKI_DIR / "log.md"

_FM_RE   = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
_H1_RE   = re.compile(r"^#\s+(.+)$", re.M)


def _project_of(rel: str) -> str:
    parts = rel.replace("\\", "/").split("/")
    if len(parts) >= 3 and parts[0] == "03- Claude" and parts[1] == "projetos":
        return parts[2]
    if len(parts) >= 2 and parts[0] == "03- Claude":
        return "03-Claude/" + parts[1]
    return parts[0]


def _parse_frontmatter(txt: str):
    """Retorna (dict_simplificado, tags:list). Sem dependência de YAML."""
    m = _FM_RE.match(txt)
    meta, tags = {}, []
    if not m:
        return meta, tags
    block = m.group(1)
    lines = block.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        # tags inline: tags: [a, b]  ou  tags: a, b
        mt = re.match(r"^\s*tags\s*:\s*(.*)$", line, re.I)
        if mt:
            val = mt.group(1).strip()
            if val.startswith("["):
                tags += [t.strip().strip("'\"") for t in val.strip("[]").split(",") if t.strip()]
            elif val:
                tags += [t.strip().strip("'\"") for t in val.split(",") if t.strip()]
            else:
                # lista YAML nas linhas seguintes:  - tag
                j = i + 1
                while j < len(lines) and re.match(r"^\s*-\s+", lines[j]):
                    tags.append(re.sub(r"^\s*-\s+", "", lines[j]).strip().strip("'\""))
                    j += 1
                i = j - 1
            i += 1
            continue
        mk = re.match(r"^\s*(title|type|tipo|updated|created|description)\s*:\s*(.+)$", line, re.I)
        if mk:
            meta[mk.group(1).lower()] = mk.group(2).strip().strip("'\"")
        i += 1
    tags = [t for t in tags if t and not t.startswith("#")]
    return meta, tags


def _title_of(txt: str, meta: dict, stem: str) -> str:
    if meta.get("title"):
        return meta["title"]
    h = _H1_RE.search(txt)
    if h:
        return h.group(1).strip()
    return stem


def scan():
    """Varre o vault e retorna a lista de páginas com metadados."""
    pages = []
    for p in MEMORY_ROOT.rglob("*.md"):
        if not p.is_file():
            continue
        try:
            txt = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        rel = str(p.relative_to(MEMORY_ROOT))
        meta, tags = _parse_frontmatter(txt)
        pages.append({
            "rel": rel, "stem": p.stem, "project": _project_of(rel),
            "title": _title_of(txt, meta, p.stem), "tags": tags,
            "type": meta.get("type") or meta.get("tipo") or "",
            "updated": meta.get("updated") or meta.get("created") or "",
            "mtime": p.stat().st_mtime, "words": len(txt.split()),
        })
    return pages


def build() -> dict:
    VAULT_WIKI_DIR.mkdir(parents=True, exist_ok=True)
    pages = scan()
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    today = datetime.now().strftime("%Y-%m-%d")

    # Agrupamentos
    by_proj, tag_pages = {}, {}
    for pg in pages:
        by_proj.setdefault(pg["project"], []).append(pg)
        for t in pg["tags"]:
            tag_pages.setdefault(t, []).append(pg["stem"])
    total_tags = len(tag_pages)
    total_words = sum(pg["words"] for pg in pages)

    # ── index.md ──────────────────────────────────────────────
    idx = [
        "---", "title: Vault-Wiki — Índice Geral", "tags: [wiki, indice, vault]",
        "type: index", f"updated: '{today}'", "---", "",
        "# Vault-Wiki — Catálogo de Todo o Claude Memory", "",
        "> Aplicação do conceito de wiki (Belchior) a todo o vault.", "",
        f"**Total de páginas:** {len(pages)}  ·  **Áreas:** {len(by_proj)}  ·  "
        f"**Tags únicas:** {total_tags}  ·  **Palavras:** {total_words:,}".replace(",", "."), "",
        "## Páginas por Área", "",
    ]
    for proj in sorted(by_proj, key=lambda k: -len(by_proj[k])):
        idx.append(f"### {proj} ({len(by_proj[proj])})")
        for pg in sorted(by_proj[proj], key=lambda x: x["title"].lower())[:60]:
            tg = f"  `{' '.join('#'+t for t in pg['tags'][:4])}`" if pg["tags"] else ""
            idx.append(f"- [[{pg['stem']}|{pg['title']}]]{tg}")
        if len(by_proj[proj]) > 60:
            idx.append(f"- … e mais {len(by_proj[proj])-60} páginas")
        idx.append("")
    idx += ["---", f"**Última atualização:** {stamp}", f"**Total de páginas:** {len(pages)}"]
    IDX_FILE.write_text("\n".join(idx), encoding="utf-8")

    # ── status.md (resumo executivo + cobertura de tags) ──────
    sta = [
        "---", "name: vault-wiki-status",
        "description: Vault-Wiki — status de todo o Claude Memory", "type: status",
        f"updated: '{today}'", "---", "",
        "# Vault-Wiki — Status", "", f"**Atualizado:** {stamp}", "",
        "## Resumo Executivo",
        f"- **Total de páginas:** {len(pages)}",
        f"- **Áreas/projetos:** {len(by_proj)}",
        f"- **Tags únicas:** {total_tags}",
        f"- **Palavras totais:** {total_words:,}".replace(",", "."), "",
        "## Páginas por Área", "", "| Área | Páginas |", "|------|--------:|",
    ]
    for proj in sorted(by_proj, key=lambda k: -len(by_proj[k])):
        sta.append(f"| {proj} | {len(by_proj[proj])} |")
    sta += ["", "## Cobertura de Tags", "",
            "| Tag | Páginas | Exemplos |", "|-----|--------:|----------|"]
    for tag, stems in sorted(tag_pages.items(), key=lambda x: -len(x[1]))[:40]:
        ex = ", ".join(stems[:3])
        sta.append(f"| {tag} | {len(stems)} | {ex[:60]} |")
    STA_FILE.write_text("\n".join(sta), encoding="utf-8")

    # ── log.md (append no topo) ───────────────────────────────
    entry = (f"## {stamp} — BUILD\n"
             f"- Páginas: {len(pages)} · Áreas: {len(by_proj)} · Tags: {total_tags}\n\n")
    prev = LOG_FILE.read_text(encoding="utf-8") if LOG_FILE.exists() else "# Vault-Wiki — Log de Operações\n\n"
    if not prev.startswith("# Vault-Wiki"):
        prev = "# Vault-Wiki — Log de Operações\n\n" + prev
    head, _, tail = prev.partition("\n\n")
    LOG_FILE.write_text(head + "\n\n" + entry + tail, encoding="utf-8")

    return {
        "pages": len(pages), "areas": len(by_proj), "tags": total_tags,
        "words": total_words,
        "index": str(IDX_FILE.relative_to(MEMORY_ROOT)),
        "status": str(STA_FILE.relative_to(MEMORY_ROOT)),
        "speech": (f"Vault-Wiki gerado: {len(pages)} páginas em {len(by_proj)} áreas, "
                   f"{total_tags} tags únicas catalogadas."),
    }
