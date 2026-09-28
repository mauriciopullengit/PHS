"""
Índice de memória do Jarvis — busca por palavra-chave (instantânea) sobre o
vault Claude Memory. Leitura de todo o vault; escrita restrita a 03- Claude.

- Indexa .md e .txt recursivamente (PDFs ficam de fora).
- Chunking por headings de markdown / parágrafos.
- Busca TF com normalização de acentos e stopwords PT.
"""
import re
import threading
import unicodedata
from pathlib import Path
from datetime import datetime

MEMORY_ROOT = Path(r"C:\Users\mau\OneDrive\Documents\Claude Memory")
# Escrita permitida somente nesta subárvore (regra filePermissions do CLAUDE.md)
WRITE_ROOT  = MEMORY_ROOT / "03- Claude"
NOTES_DIR   = WRITE_ROOT / "memory" / "jarvis-notes"

_STOPWORDS = {
    "de","a","o","que","e","do","da","em","um","para","com","nao","uma","os","no",
    "se","na","por","mais","as","dos","como","mas","ao","ele","das","seu","sua","ou",
    "quando","muito","nos","ja","eu","tambem","so","pelo","pela","ate","isso","ela",
    "entre","depois","sem","mesmo","aos","seus","quem","nas","me","esse","eles","voce",
    "essa","num","nem","suas","meu","minha","numa","pelos","elas","qual","sao","of","the",
}

def _norm(text: str) -> str:
    """Minúsculas + remove acentos."""
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return text.lower()

def _tokens(text: str):
    return [t for t in re.findall(r"[a-z0-9]{3,}", _norm(text)) if t not in _STOPWORDS]


class MemoryIndex:
    def __init__(self):
        self.chunks = []          # [{path, rel, title, heading, text, tf}]
        self.ready = False
        self.files = 0
        self.error = None
        self._lock = threading.Lock()

    # ── Construção do índice ────────────────────────────────────────────
    def build(self):
        try:
            chunks = []
            files = 0
            if not MEMORY_ROOT.exists():
                self.error = f"Pasta não encontrada: {MEMORY_ROOT}"
                return
            for path in MEMORY_ROOT.rglob("*"):
                if path.suffix.lower() not in (".md", ".txt"):
                    continue
                if not path.is_file():
                    continue
                try:
                    raw = path.read_text(encoding="utf-8", errors="replace")
                except Exception:
                    continue
                files += 1
                rel = str(path.relative_to(MEMORY_ROOT))
                title = path.stem
                for heading, body in self._split(raw):
                    body = body.strip()
                    if len(body) < 40:
                        continue
                    tf = {}
                    for tok in _tokens(title + " " + heading + " " + body):
                        tf[tok] = tf.get(tok, 0) + 1
                    if tf:
                        chunks.append({
                            "path": str(path), "rel": rel, "title": title,
                            "heading": heading, "text": body[:1200], "tf": tf,
                        })
            with self._lock:
                self.chunks = chunks
                self.files = files
                self.ready = True
                self.error = None
        except Exception as exc:
            self.error = str(exc)

    def build_async(self):
        threading.Thread(target=self.build, daemon=True).start()

    @staticmethod
    def _split(raw: str):
        """Divide por headings markdown; parágrafos longos viram janelas ~700 chars."""
        parts = re.split(r"^(#{1,6}\s+.*)$", raw, flags=re.M)
        # parts: [pre, heading1, body1, heading2, body2, ...]
        out = []
        if parts and parts[0].strip():
            out.append(("", parts[0]))
        i = 1
        while i < len(parts):
            heading = parts[i].lstrip("#").strip()
            body = parts[i + 1] if i + 1 < len(parts) else ""
            i += 2
            if len(body) > 1400:
                for j in range(0, len(body), 700):
                    out.append((heading, body[j:j + 900]))
            else:
                out.append((heading, body))
        return out

    # ── Busca ───────────────────────────────────────────────────────────
    def search(self, query: str, k: int = 5):
        with self._lock:
            chunks = self.chunks
        q = _tokens(query)
        if not q or not chunks:
            return []
        qset = set(q)
        scored = []
        for c in chunks:
            tf = c["tf"]
            score = 0.0
            hits = 0
            for tok in qset:
                if tok in tf:
                    score += tf[tok]
                    hits += 1
            if hits == 0:
                continue
            # bônus por cobertura de termos + match no título
            score *= (1 + hits / len(qset))
            if any(tok in _norm(c["title"]) for tok in qset):
                score *= 1.5
            scored.append((score, c))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [
            {"rel": c["rel"], "title": c["title"], "heading": c["heading"], "text": c["text"], "score": round(s, 2)}
            for s, c in scored[:k]
        ]

    def context_block(self, query: str, k: int = 5, max_chars: int = 3500) -> str:
        """Monta bloco de contexto para injetar no prompt do LLM."""
        results = self.search(query, k)
        if not results:
            return ""
        blocks, total = [], 0
        for r in results:
            head = f" › {r['heading']}" if r["heading"] else ""
            snippet = f"[Fonte: {r['rel']}{head}]\n{r['text'].strip()}"
            if total + len(snippet) > max_chars:
                break
            blocks.append(snippet)
            total += len(snippet)
        return "\n\n".join(blocks)

    # ── Escrita (somente em 03- Claude) ─────────────────────────────────
    @staticmethod
    def save_note(title: str, content: str) -> dict:
        NOTES_DIR.mkdir(parents=True, exist_ok=True)
        slug = re.sub(r"[^a-z0-9]+", "-", _norm(title)).strip("-")[:50] or "nota"
        stamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        fname = f"{stamp}-{slug}.md"
        dest = NOTES_DIR / fname
        body = (
            f"---\ndata: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
            f"origem: Jarvis (Francisca)\n---\n\n# {title}\n\n{content}\n"
        )
        dest.write_text(body, encoding="utf-8")
        return {"saved": True, "file": str(dest), "rel": str(dest.relative_to(MEMORY_ROOT))}


# Instância global
INDEX = MemoryIndex()
