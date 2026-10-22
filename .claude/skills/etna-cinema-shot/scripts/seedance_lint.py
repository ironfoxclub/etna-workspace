#!/usr/bin/env python3
"""
seedance_lint.py
================
Pre-flight linter for Seedance 2.0 / Seedance Pro prompts.

Seedance's content filter is an LLM reading full-scene intent, not a keyword
blacklist. But it still reliably flags prompts on a handful of patterns — this
linter catches those patterns before the user burns credits on an instant-fail.

Rules are grouped into three severities:
  FAIL  — will almost certainly be flagged. Do not generate.
  WARN  — likely to pass but weak; harden before generating.
  INFO  — style suggestion, not a flag risk.

Usage:
  python3 seedance_lint.py "<prompt text>"
  echo "<prompt text>" | python3 seedance_lint.py
  python3 seedance_lint.py --file prompt.txt
  python3 seedance_lint.py --log "<prompt text>"      # log FAIL to filter-memory
  python3 seedance_lint.py --confirmed "<prompt>"     # log as confirmed workaround

Exit codes: 0 = PASS or WARN only, 1 = any FAIL.

Filter-memory loopback:
  --log         → on FAIL, append an entry to db/filter-memory.json with
                  outcome=unknown. Rule hits become blocked_terms + tags.
  --confirmed   → append the prompt as a confirmed workaround (outcome=
                  workaround, substitution_worked=True). Use after a rewrite
                  passes Seedance's filter in a real generation.

  Para mudar o resultado de uma entrada depois, edite o campo "outcome" dela no JSON.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


# ── Rule data ───────────────────────────────────────────────────────────────

# Real person / public figure name patterns. Not exhaustive — Seedance's filter
# has a much larger list internally — but these are the ones users repeatedly
# hit in our filter-memory database.
REAL_NAMES = [
    r"\belon musk\b", r"\bdonald trump\b", r"\bjoe biden\b", r"\bkamala harris\b",
    r"\bvladimir putin\b", r"\bxi jinping\b", r"\bbarack obama\b",
    r"\bkeanu reeves\b", r"\btom cruise\b", r"\bbrad pitt\b", r"\bdicaprio\b",
    r"\btaylor swift\b", r"\bbeyonc[eé]\b", r"\brihanna\b", r"\bkanye\b", r"\bye\b(?! olde)",
    r"\bkim kardashian\b", r"\bdrake\b(?!'s equation)", r"\btravis scott\b",
    r"\bmessi\b", r"\bronaldo\b", r"\blebron\b", r"\bmichael jordan\b",
    r"\bmr beast\b", r"\bmrbeast\b",
]

# Brands, IPs, trademarked characters. Same story — representative, not exhaustive.
BRANDS_IP = [
    r"\bnike\b", r"\badidas\b", r"\bpuma\b", r"\bgucci\b", r"\bprada\b", r"\blouis vuitton\b",
    r"\bcoca[- ]cola\b", r"\bpepsi\b", r"\bmcdonald'?s\b", r"\bstarbucks\b",
    r"\bapple\b(?! (pie|tree|orchard|falls|juice))", r"\biphone\b", r"\bmacbook\b",
    r"\bgoogle\b", r"\bmicrosoft\b", r"\bwindows\b(?! (are|were|of|into|into))",
    r"\btesla\b", r"\bferrari\b", r"\blamborghini\b", r"\bporsche\b", r"\brolex\b",
    r"\bmarvel\b", r"\bdc comics\b", r"\bdisney\b", r"\bpixar\b", r"\bdreamworks\b",
    r"\bspider[- ]?man\b", r"\bbatman\b", r"\bsuperman\b", r"\biron man\b",
    r"\bcaptain america\b", r"\bthor\b", r"\bhulk\b", r"\bblack widow\b",
    r"\bwolverine\b", r"\bdeadpool\b", r"\bharry potter\b", r"\bhogwarts\b",
    r"\bpok[eé]mon\b", r"\bpikachu\b", r"\bmario\b", r"\bsonic\b",
    r"\bstar wars\b", r"\bjedi\b", r"\bsith\b", r"\bdarth vader\b",
    r"\bjames bond\b", r"\b007\b",
]

# Raw violence / harm verbs. Seedance flags the verb, not the concept — the
# concept can be rendered cinematically via aftermath/tension/physics.
VIOLENCE_VERBS = [
    r"\bkill(s|ed|ing)?\b", r"\bmurder(s|ed|ing)?\b", r"\bassassinat(e|es|ed|ing)\b",
    r"\bstab(s|bed|bing)?\b", r"\bshoot(s|ing)?\b", r"\bshot\b",
    r"\bslash(es|ed|ing)?\b", r"\bbehead(s|ed|ing)?\b", r"\bdecapitat(e|es|ed|ing)\b",
    r"\btortur(e|es|ed|ing)\b", r"\brap(e|es|ed|ing)\b",
    r"\bblood(y|ied|ying)?\b", r"\bgore\b", r"\bgory\b", r"\bgutted?\b",
    r"\bdismember(s|ed|ing)?\b", r"\bmutilat(e|es|ed|ing)\b",
    r"\bfight(s|ing)?\b", r"\battack(s|ed|ing)?\b", r"\bpunch(es|ed|ing)?\b",
    r"\bbeating\b", r"\bbeat(s|en)?\b(?! (the|up the) (rug|eggs|drum|heat|path|odds))",
]

WEAPON_NOUNS = [
    r"\bgun\b", r"\brifle\b", r"\bpistol\b", r"\bshotgun\b", r"\bhandgun\b",
    r"\bmachine gun\b", r"\bak[- ]?47\b", r"\bm16\b", r"\buzi\b",
    r"\bknife\b", r"\bdagger\b", r"\bsword\b(?! (fern|fish|dance))",
    r"\bbomb\b", r"\bgrenade\b", r"\bexplosive\b",
]

AGE_MARKERS = [
    r"\bchild(ren)?\b", r"\bkid(s|dies)?\b", r"\bbaby\b", r"\binfant\b", r"\btoddler\b",
    r"\bboy(s)?\b", r"\bgirl(s)?\b", r"\bteen(ager|agers|aged)?\b",
    r"\byoung (man|woman|boy|girl)\b", r"\blittle (boy|girl|kid|child)\b",
    r"\bminor(s)?\b(?! (chord|key|scale|league|issue|detail))",
    r"\bschoolboy\b", r"\bschoolgirl\b", r"\bpreschool(er)?\b",
]

# Antislop — marketing-copy adjectives that correlate with vague prompts and
# therefore with filter flags. Warn, don't fail.
ANTISLOP = [
    r"\bbreathtaking\b", r"\bstunning\b", r"\bepic\b", r"\bmesmerizing\b",
    r"\bawe[- ]inspiring\b", r"\bmasterfully\b", r"\bmeticulously\b",
    r"\bexquisitely\b", r"\bbeautifully crafted\b", r"\bcinematic masterpiece\b",
    r"\bvisual feast\b", r"\bseamlessly\b", r"\beffortlessly\b", r"\bflawlessly\b",
    r"\bcutting[- ]edge\b", r"\bstate[- ]of[- ]the[- ]art\b",
    r"\bmind[- ]blowing\b", r"\bjaw[- ]dropping\b",
]

# Sections the filter wants to see — presence of these clauses strongly
# correlates with passing. Detected by keyword cues, not strict parsing.
STYLE_MOOD_CUES = [
    "style", "mood", "palette", "color grade", "lighting", "atmosphere",
    "golden hour", "blue hour", "overcast", "neon", "practical", "noir",
    "desaturated", "teal and orange", "high contrast", "low[- ]key",
    "anamorphic", "vhs", "super 8", "cinematic",
]
CAMERA_CUES = [
    "camera", "dolly", "tracking", "pan", "tilt", "crane", "steadicam",
    "handheld", "aerial", "drone", "pov", "push[- ]in", "pull[- ]out",
    "orbit", "whip[- ]pan", "low[- ]angle", "high[- ]angle", "overhead",
    "wide shot", "medium shot", "close[- ]up", "ecu", "ots", "over the shoulder",
]
SETTING_CUES = [
    # Any concrete noun-ish location word. Tiny heuristic — looks for common
    # location descriptors.
    "room", "hall", "street", "alley", "forest", "desert", "beach",
    "kitchen", "bedroom", "office", "warehouse", "studio", "stage",
    "city", "town", "village", "rooftop", "stairwell", "parking",
    "interior", "exterior", "indoor", "outdoor", "indoors", "outdoors",
    "at night", "by day", "at dawn", "at dusk",
]


@dataclass
class Finding:
    severity: str  # "FAIL" | "WARN" | "INFO"
    rule: str
    hit: str
    fix: str


def _matches(patterns: list[str], text: str) -> list[str]:
    hits: list[str] = []
    for pat in patterns:
        for m in re.finditer(pat, text, flags=re.IGNORECASE):
            hits.append(m.group(0))
    return hits


def _has_cue(cues: list[str], text: str) -> bool:
    lowered = text.lower()
    return any(re.search(c, lowered) for c in cues)


def lint(prompt: str) -> list[Finding]:
    findings: list[Finding] = []
    text = prompt.strip()
    word_count = len(re.findall(r"\b\w+\b", text))

    if not text:
        findings.append(Finding("FAIL", "empty", "", "O prompt está vazio."))
        return findings

    # ── FAIL rules ──────────────────────────────────────────────────────────

    hits = _matches(REAL_NAMES, text)
    if hits:
        findings.append(Finding(
            "FAIL", "real-person-name", ", ".join(sorted(set(hits))),
            "Troque o nome por um arquétipo: faixa de idade, porte, cabelo, "
            "figurino, expressão. Veja o playbook de reescrita em etna-cinema-shot."
        ))

    hits = _matches(BRANDS_IP, text)
    if hits:
        findings.append(Finding(
            "FAIL", "brand-ip", ", ".join(sorted(set(hits))),
            "Descreva só traços visuais: geometria, cor, material. Nunca "
            "cite a marca, a franquia ou o personagem pelo nome."
        ))

    hits = _matches(VIOLENCE_VERBS, text)
    if hits:
        findings.append(Finding(
            "FAIL", "violence-verb", ", ".join(sorted(set(hits))),
            "Descreva o rescaldo, a tensão, a força ou a direção, não o ato. "
            "Ex.: 'driven into the car, metal buckling' em vez de 'punches'."
        ))

    hits = _matches(WEAPON_NOUNS, text)
    if hits:
        findings.append(Finding(
            "FAIL", "weapon-noun", ", ".join(sorted(set(hits))),
            "Descreva o confronto / a silhueta / a geometria do adereço, não a "
            "arma pelo nome. O filtro lê armas nomeadas como intenção."
        ))

    hits = _matches(AGE_MARKERS, text)
    if hits:
        findings.append(Finding(
            "FAIL", "age-marker", ", ".join(sorted(set(hits))),
            "O Seedance é cego para idade. Descreva por papel + roupa + ação: "
            "'a figure in a wool cloak', 'the rider', 'the traveler'."
        ))

    if word_count > 220:
        findings.append(Finding(
            "FAIL", "overlength", f"{word_count} palavras",
            "Acima de 220 palavras o codificador de texto costuma falhar. Corte "
            "para 30–180 palavras. Mantenha Estilo e Humor + câmera + ação; corte o resto."
        ))

    # ── WARN rules ──────────────────────────────────────────────────────────

    hits = _matches(ANTISLOP, text)
    if hits:
        findings.append(Finding(
            "WARN", "antislop", ", ".join(sorted(set(hits))),
            "Adjetivos de texto publicitário se correlacionam com marcações: "
            "sinalizam intenção vaga. Troque por detalhes observáveis e mensuráveis."
        ))

    if word_count > 180:
        findings.append(Finding(
            "WARN", "long", f"{word_count} palavras",
            "Acima de 180 palavras é zona de risco. Corte os detalhes menos "
            "essenciais antes de gerar."
        ))

    if word_count < 15:
        findings.append(Finding(
            "WARN", "too-short", f"{word_count} palavras",
            "Curto demais: o filtro não tem cena para interpretar. Acrescente pelo "
            "menos Estilo e Humor + câmera + cenário para o plano ficar legível."
        ))

    if not _has_cue(STYLE_MOOD_CUES, text):
        findings.append(Finding(
            "WARN", "no-style-mood", "",
            "Nenhuma cláusula de Estilo / Humor / luz / paleta detectada. Acrescente "
            "uma frase com a paleta, a luz e a atmosfera."
        ))

    if not _has_cue(CAMERA_CUES, text):
        findings.append(Finding(
            "WARN", "no-camera", "",
            "Nenhum movimento de câmera detectado. Nomeie um movimento exato: 'slow "
            "dolly-in', 'low-angle tracking', 'static medium'. Não 'the camera moves'."
        ))

    if not _has_cue(SETTING_CUES, text):
        findings.append(Finding(
            "WARN", "no-setting", "",
            "Nenhum cenário concreto detectado. Acrescente um local para o filtro "
            "ter uma cena para interpretar (interior/exterior, tipo de cômodo, hora do dia)."
        ))

    # ── Contradictions (INFO — heuristic) ───────────────────────────────────

    lowered = text.lower()
    contradictions = [
        (("moving fast", "frozen"), "Movimento rápido + congelado na mesma cena."),
        (("bright", "pitch black"), "Claro + breu total na mesma cena."),
        (("dolly in", "dolly out"), "Dolly para dentro e dolly para fora no mesmo plano."),
        (("crane up", "crane down"), "Grua para cima e grua para baixo no mesmo plano."),
        (("zoom in", "zoom out"), "Zoom para dentro e zoom para fora no mesmo plano."),
    ]
    for (a, b), message in contradictions:
        if a in lowered and b in lowered:
            findings.append(Finding(
                "WARN", "contradiction", f"{a} + {b}",
                message + " Escolha um: divida em dois planos se precisar dos dois."
            ))

    return findings


def render(prompt: str, findings: list[Finding]) -> tuple[str, str]:
    """Return (verdict, report text). Verdict is PASS / WARN / FAIL."""
    fails = [f for f in findings if f.severity == "FAIL"]
    warns = [f for f in findings if f.severity == "WARN"]

    if fails:
        verdict = "FAIL"
    elif warns:
        verdict = "WARN"
    else:
        verdict = "PASS"

    lines: list[str] = []
    lines.append(f"Pré-voo Seedance — {verdict}")
    lines.append("=" * 40)
    word_count = len(re.findall(r"\b\w+\b", prompt.strip()))
    lines.append(f"  palavras: {word_count}")
    lines.append("")

    if not findings:
        lines.append("  Nenhum problema detectado. A cena lê como um plano de cinema.")
        lines.append("  Pode gerar.")
        return verdict, "\n".join(lines)

    for f in findings:
        tag = {"FAIL": "✗", "WARN": "⚠", "INFO": "·"}[f.severity]
        head = f"  {tag} [{f.severity}] {f.rule}"
        if f.hit:
            head += f" — {f.hit}"
        lines.append(head)
        lines.append(f"      conserto: {f.fix}")
        lines.append("")

    if verdict == "FAIL":
        lines.append("  NÃO gere. Aplique os consertos acima e rode o linter de novo.")
    elif verdict == "WARN":
        lines.append("  Provavelmente passa, mas reforce os pontos fracos antes.")

    return verdict, "\n".join(lines)


# Memória do filtro: um JSON simples ao lado do script (db/filter-memory.json).
# ponytail: arquivo único sem trava; se vários painéis gravarem juntos, trocar por um arquivo por entrada.
FILTER_DB = Path(os.environ.get("ETNA_FILTER_MEMORY") or Path(__file__).parent.parent / "db" / "filter-memory.json")


def load_db(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"entries": []}


def save_db(path: Path, db: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding="utf-8")


def next_id(entries: list, prefix: str) -> str:
    nums = [int(e["id"][len(prefix):]) for e in entries if str(e.get("id", "")).startswith(prefix)]
    return f"{prefix}{max(nums, default=0) + 1:03d}"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def log_to_filter_memory(prompt: str, findings: list[Finding], confirmed: bool) -> str:
    """Acrescenta uma entrada em db/filter-memory.json e devolve o id novo."""
    db = load_db(FILTER_DB)

    fails = [f for f in findings if f.severity == "FAIL"]
    warns = [f for f in findings if f.severity == "WARN"]

    categories = sorted({f.rule for f in fails}) or ["preflight-warn"]
    blocked = sorted({f.hit for f in fails if f.hit})
    fixes = "; ".join(f.fix for f in fails) or "; ".join(f.fix for f in warns)

    entry = {
        "id": next_id(db["entries"], "F"),
        "date_added": now_iso(),
        "category": categories[0],
        "blocked_terms": blocked,
        "error_message": (
            "Linter de pré-voo do Seedance (contorno confirmado)"
            if confirmed
            else "Linter de pré-voo do Seedance previu reprovação do filtro"
        ),
        "failed_prompt": prompt.strip()[:600],
        "substitution": fixes or None,
        "substitution_worked": True if confirmed else None,
        "fix_confirmed": confirmed,
        "outcome": "workaround" if confirmed else "unknown",
        "tags": ["seedance-2.0", "preflight-linter"] + categories,
        "notes": "",
    }

    db["entries"].append(entry)
    try:
        save_db(FILTER_DB, db)
    except OSError as e:  # log é opcional: pasta só de leitura não derruba o lint
        return f"{entry['id']} (NÃO gravou: {e.strerror or e})"
    return entry["id"]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Linter de pré-voo para prompts do Seedance 2.0."
    )
    parser.add_argument("prompt", nargs="?", help="Texto do prompt (ou use --file / stdin)")
    parser.add_argument("--file", "-f", help="Lê o prompt de um arquivo")
    parser.add_argument("--log", action="store_true",
                        help="Em caso de FALHA, grava uma entrada em db/filter-memory.json")
    parser.add_argument("--confirmed", action="store_true",
                        help="Grava o prompt como contorno de filtro confirmado "
                             "(outcome=workaround, substitution_worked=True)")
    args = parser.parse_args()

    if args.file:
        prompt = open(args.file, encoding="utf-8").read()
    elif args.prompt:
        prompt = args.prompt
    elif not sys.stdin.isatty():
        prompt = sys.stdin.read()
    else:
        parser.print_help()
        return 2

    findings = lint(prompt)
    verdict, report = render(prompt, findings)
    print(report)

    if args.confirmed:
        entry_id = log_to_filter_memory(prompt, findings, confirmed=True)
        print(f"\n  gravado como contorno confirmado → {entry_id}")
    elif args.log and verdict == "FAIL":
        entry_id = log_to_filter_memory(prompt, findings, confirmed=False)
        print(f"\n  gravado no filter-memory → {entry_id}")

    return 1 if verdict == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
