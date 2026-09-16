"""
Operações de wiki do Jarvis sobre TODO o vault Claude Memory.
Adaptação da skill `wiki` (Belchior) para o vault inteiro estilo Obsidian.

Comandos: STATUS, PENDING, QUERY, LINT, INGEST.
- Leitura: todo o vault.  Escrita: somente 03- Claude (regra filePermissions).
"""
import re
from pathlib import Path
from datetime import datetime

from memory_index import MEMORY_ROOT, WRITE_ROOT, INDEX

WIKI_DIR  = WRITE_ROOT / "Wiki" / "Jarvis"      # destino de INGEST
WIKI_INDEX = WIKI_DIR / "index.md"

_LINK_RE = re.compile(r"\[\[([^\]\|#]+)")
_TODO_RE = re.compile(r"^\s*[-*]\s+\[ \]\s+(.*)$")


def _md_files():
    return [p for p in MEMORY_ROOT.rglob("*.md") if p.is_file()]


def _project_of(rel: str) -> str:
    parts = rel.replace("\\", "/").split("/")
    if len(parts) >= 3 and parts[0] == "03- Claude" and parts[1] == "projetos":
        return parts[2]
    if len(parts) >= 2 and parts[0] == "03- Claude":
        return "03-Claude/" + parts[1]
    return parts[0]


# ── STATUS ────────────────────────────────────────────────────────────────────
def status() -> dict:
    files = _md_files()
    projects, total_words, total_links, with_todos = {}, 0, 0, 0
    recent = []
    for p in files:
        try:
            txt = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        rel = str(p.relative_to(MEMORY_ROOT))
        proj = _project_of(rel)
        projects[proj] = projects.get(proj, 0) + 1
        total_words += len(txt.split())
        total_links += len(_LINK_RE.findall(txt))
        if any(_TODO_RE.match(l) for l in txt.splitlines()):
            with_todos += 1
        recent.append((p.stat().st_mtime, rel))
    recent.sort(reverse=True)
    top_projects = sorted(projects.items(), key=lambda x: -x[1])
    detail = ["# Status do Vault (Claude Memory)\n",
              f"- Notas .md: **{len(files)}**",
              f"- Trechos indexados: **{len(INDEX.chunks)}**",
              f"- Palavras totais: **{total_words:,}**".replace(",", "."),
              f"- Wikilinks [[ ]]: **{total_links}**",
              f"- Notas com tarefas abertas: **{with_todos}**\n",
              "## Projetos / áreas"]
    for name, n in top_projects[:12]:
        detail.append(f"- {name}: {n} notas")
    detail.append("\n## Modificadas recentemente")
    for _, rel in recent[:5]:
        detail.append(f"- {rel}")
    speech = (f"O vault tem {len(files)} notas em {len(projects)} áreas, "
              f"{total_words} palavras e {with_todos} notas com tarefas abertas.")
    return {"speech": speech, "detail": "\n".join(detail)}


# ── PENDING (tarefas abertas em todo o vault) ────────────────────────────────
def pending(limit: int = 40) -> dict:
    items = []
    for p in _md_files():
        try:
            lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
        except Exception:
            continue
        rel = str(p.relative_to(MEMORY_ROOT))
        for l in lines:
            m = _TODO_RE.match(l)
            if m and m.group(1).strip():
                items.append((_project_of(rel), rel, m.group(1).strip()))
    detail = [f"# Tarefas abertas no vault ({len(items)})\n"]
    by_proj = {}
    for proj, rel, task in items:
        by_proj.setdefault(proj, []).append((rel, task))
    shown = 0
    for proj in sorted(by_proj, key=lambda k: -len(by_proj[k])):
        detail.append(f"## {proj} ({len(by_proj[proj])})")
        for rel, task in by_proj[proj][:12]:
            detail.append(f"- [ ] {task}  ·  _{Path(rel).name}_")
            shown += 1
            if shown >= limit:
                break
        if shown >= limit:
            detail.append(f"\n… e mais {len(items)-shown} tarefas.")
            break
    speech = f"Você tem {len(items)} tarefas abertas em {len(by_proj)} áreas do vault."
    return {"speech": speech, "detail": "\n".join(detail)}


# ── LINT (saúde do vault) ────────────────────────────────────────────────────
def lint() -> dict:
    files = _md_files()
    names = {p.stem.lower() for p in files}
    incoming = {p.stem.lower(): 0 for p in files}
    broken, no_fm = [], []
    for p in files:
        try:
            txt = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        rel = str(p.relative_to(MEMORY_ROOT))
        if not txt.lstrip().startswith("---"):
            no_fm.append(rel)
        for target in _LINK_RE.findall(txt):
            t = target.strip().lower()
            if t in incoming:
                incoming[t] += 1
            elif t and t not in names:
                broken.append((rel, target.strip()))
    HUBS = ("index", "memory", "dashboard", "readme", "pending", "decisions")
    orphans = [p for p in files
               if incoming.get(p.stem.lower(), 0) == 0
               and not any(h in p.stem.lower() for h in HUBS)]
    detail = ["# Lint do Vault\n",
              f"- Links quebrados: **{len(broken)}**",
              f"- Notas órfãs (sem links de entrada): **{len(orphans)}**",
              f"- Notas sem frontmatter: **{len(no_fm)}**\n"]
    if broken:
        detail.append("## Links quebrados (amostra)")
        for rel, tgt in broken[:12]:
            detail.append(f"- [[{tgt}]] em _{Path(rel).name}_")
    if orphans:
        detail.append("\n## Órfãs (amostra)")
        for p in orphans[:12]:
            detail.append(f"- {p.relative_to(MEMORY_ROOT)}")
    speech = (f"Encontrei {len(broken)} links quebrados, {len(orphans)} notas órfãs "
              f"e {len(no_fm)} notas sem frontmatter.")
    return {"speech": speech, "detail": "\n".join(detail)}


# ── QUERY (RAG + síntese via Groq) ───────────────────────────────────────────
def query(question: str, groq_client=None, model: str = "") -> dict:
    results = INDEX.search(question, k=6)
    if not results:
        return {"speech": "Não encontrei nada no vault sobre isso.",
                "detail": "Nenhuma fonte encontrada no vault.", "sources": []}
    ctx = INDEX.context_block(question, k=6)
    answer = ""
    if groq_client and model:
        try:
            comp = groq_client.chat.completions.create(
                model=model, max_tokens=400,
                messages=[
                    {"role": "system", "content":
                     "Você é Francisca. Responda à pergunta em PT-BR de forma concisa "
                     "(até 4 frases) usando SOMENTE o contexto do vault fornecido. "
                     "Cite as fontes relevantes pelo nome do arquivo."},
                    {"role": "user", "content": f"Contexto:\n{ctx}\n\nPergunta: {question}"},
                ])
            answer = comp.choices[0].message.content.strip()
        except Exception as exc:
            answer = f"(Erro ao sintetizar: {exc})"
    sources = [{"rel": r["rel"], "heading": r["heading"]} for r in results]
    detail = [answer or "Fontes encontradas:", "\n## Fontes"]
    for r in results:
        head = f" › {r['heading']}" if r["heading"] else ""
        detail.append(f"- {r['rel']}{head}")
    speech = answer or f"Encontrei {len(results)} fontes no vault sobre isso."
    return {"speech": speech, "detail": "\n".join(detail), "sources": sources}


# ── INGEST (cria nota estruturada com frontmatter + atualiza index) ──────────
def ingest(title: str, content: str, tags=None, source: str = "") -> dict:
    WIKI_DIR.mkdir(parents=True, exist_ok=True)
    tags = tags or []
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:60] or "nota"
    dest = WIKI_DIR / f"{slug}.md"
    fm = ["---", f"title: {title}",
          f"tags: [{', '.join(tags)}]" if tags else "tags: []",
          f"sources: {source}" if source else "sources: ",
          f"updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
          "origem: Jarvis (Francisca)", "---", "", f"# {title}", "", content.strip(), ""]
    dest.write_text("\n".join(fm), encoding="utf-8")
    # Atualiza index
    line = f"- [[{slug}|{title}]] — {datetime.now().strftime('%Y-%m-%d')}\n"
    if WIKI_INDEX.exists():
        WIKI_INDEX.write_text(WIKI_INDEX.read_text(encoding="utf-8") + line, encoding="utf-8")
    else:
        WIKI_INDEX.write_text("# Índice Wiki Jarvis\n\n" + line, encoding="utf-8")
    INDEX.build_async()
    return {"saved": True, "rel": str(dest.relative_to(MEMORY_ROOT)),
            "speech": f"Página '{title}' criada no wiki e indexada."}
