#!/usr/bin/env python3
"""Convert expanded_thesis_fa.md to LaTeX chapter files."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MD_PATH = ROOT / "new-ideas" / "expanded_thesis_fa.md"
OUT_DIR = ROOT / "thesis_latex_sample"

IMAGE_MAP = {
    "taxonomy_blockchain_scaling.png": ("taxonomy_blockchain_scaling.png", "fig:scaling-taxonomy"),
    "architecture_master_sidechain.png": ("architecture_master_sidechain.png", "fig:architecture-overview"),
    "tps_scalability.png": ("tps_vs_sidechains.png", "fig:tps-scalability"),
}

SPECIAL_TABLE_2_1 = r"""\begin{table}[h]
\centering
\caption{مقایسه خانواده‌های مقیاس‌پذیری}
\label{tab:scaling-taxonomy}
\small
\includegraphics[width=0.98\linewidth]{img/taxonomy_table_2-1.png}
\end{table}
"""

SPECIAL_TAXONOMY_FIG = r"""\begin{figure}[h]
\centering
\includegraphics[width=0.95\linewidth]{img/taxonomy_blockchain_scaling.png}
\caption{تکسونومی روش‌های مقیاس‌پذیری بلاکچین}
\label{fig:scaling-taxonomy}
\end{figure}
"""


def persian_to_ascii_digits(s: str) -> str:
    trans = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")
    return s.translate(trans)


INLINE_MATH_RE = re.compile(r"\\\(.+?\\\)")


def escape_latex_text(s: str) -> str:
    """Escape LaTeX special chars in plain text (not math/commands)."""
    result = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == "\\":
            result.append(r"\textbackslash{}")
        elif c == "&":
            result.append(r"\&")
        elif c == "%":
            result.append(r"\%")
        elif c == "#":
            result.append(r"\#")
        elif c == "_":
            result.append(r"\_")
        elif c == "{":
            result.append(r"\{")
        elif c == "}":
            result.append(r"\}")
        elif c == "~":
            result.append(r"\textasciitilde{}")
        elif c == "^":
            result.append(r"\textasciicircum{}")
        else:
            result.append(c)
        i += 1
    return "".join(result)


def split_inline_math(text: str) -> list[tuple[str, str]]:
    """Split text into ('text', ...) and ('math', ...) segments."""
    parts: list[tuple[str, str]] = []
    last = 0
    for m in INLINE_MATH_RE.finditer(text):
        if m.start() > last:
            parts.append(("text", text[last : m.start()]))
        parts.append(("math", m.group(0)))
        last = m.end()
    if last < len(text):
        parts.append(("text", text[last:]))
    return parts or [("text", text)]


def process_plain_text(text: str) -> str:
    """Markdown inline formatting on non-math segments only."""
    chunks: list[str] = []
    pos = 0
    pattern = re.compile(r"\*\*(.+?)\*\*|`([^`]+)`")
    for m in pattern.finditer(text):
        if m.start() > pos:
            chunks.append(escape_latex_text(text[pos : m.start()]))
        if m.group(1) is not None:
            inner = []
            for kind, chunk in split_inline_math(m.group(1)):
                if kind == "math":
                    inner.append(chunk)
                else:
                    inner.append(escape_latex_text(chunk))
            chunks.append(r"\textbf{" + "".join(inner) + "}")
        else:
            chunks.append(r"\lr{" + escape_latex_text(m.group(2)) + "}")
        pos = m.end()
    if pos < len(text):
        chunks.append(escape_latex_text(text[pos:]))
    return "".join(chunks)


def process_inline(text: str) -> str:
    """Convert markdown inline formatting to LaTeX, preserving \\( ... \\)."""
    chunks = []
    for kind, chunk in split_inline_math(text):
        if kind == "math":
            chunks.append(chunk)
        else:
            chunks.append(process_plain_text(chunk))
    return "".join(chunks)


def parse_table_row(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


def col_alignments(sep_row: list[str]) -> list[str]:
    aligns = []
    for cell in sep_row:
        cell = cell.strip()
        if cell.startswith(":") and cell.endswith(":"):
            aligns.append("c")
        elif cell.endswith(":"):
            aligns.append("r")
        elif cell.startswith(":"):
            aligns.append("l")
        else:
            aligns.append("p{2.2cm}")
    return aligns


def build_tabular(header: list[str], rows: list[list[str]], aligns: list[str]) -> str:
    n = len(header)
    if n <= 2:
        col_spec = "|" + "|".join(["p{5.5cm}", "p{8cm}"][:n]) + "|"
    elif n == 3:
        col_spec = "|p{3.5cm}|p{4.5cm}|p{5.5cm}|"
    elif n == 4:
        col_spec = "|p{2.8cm}|p{3.2cm}|p{3.2cm}|p{3.5cm}|"
    elif n == 5:
        col_spec = "|p{2.2cm}|p{2.8cm}|p{2.5cm}|p{2.8cm}|p{2.8cm}|"
    elif n == 6:
        col_spec = "|p{1.8cm}|p{1.6cm}|p{1.6cm}|p{1.6cm}|p{1.6cm}|p{1.8cm}|"
    elif n == 7:
        col_spec = "|p{1.4cm}|p{1.5cm}|p{1.5cm}|p{1.5cm}|p{1.5cm}|p{1.5cm}|p{1.6cm}|"
    else:
        col_spec = "|" + "|".join(["p{2cm}"] * n) + "|"

    lines = [r"\begin{tabular}{" + col_spec + "}", r"\hline"]
    lines.append(" & ".join(process_inline(h) for h in header) + r" \\")
    lines.append(r"\hline")
    for row in rows:
        padded = row + [""] * (n - len(row))
        lines.append(" & ".join(process_inline(c) for c in padded[:n]) + r" \\")
        lines.append(r"\hline")
    lines.append(r"\end{tabular}")
    return "\n".join(lines)


def figure_latex(alt: str, img_file: str, label: str) -> str:
    cap = escape_latex_text(alt)
    return (
        f"\\begin{{figure}}[h]\n"
        f"\\centering\n"
        f"\\includegraphics[width=0.92\\linewidth]{{img/{img_file}}}\n"
        f"\\caption{{{cap}}}\n"
        f"\\label{{{label}}}\n"
        f"\\end{{figure}}\n"
    )


class Converter:
    def __init__(self, text: str):
        self.lines = text.splitlines()
        self.out: list[str] = []
        self.i = 0
        self.pending_caption: str | None = None
        self.in_section_2_13 = False
        self.skip_table_2_1 = False

    def convert(self) -> str:
        while self.i < len(self.lines):
            line = self.lines[self.i]
            stripped = line.strip()

            if not stripped:
                if self.out and self.out[-1] != "":
                    self.out.append("")
                self.i += 1
                continue

            # Section headers
            m_sec = re.match(r"^##\s+([۰-۹0-9]+-[۰-۹0-9]+(?:-[۰-۹0-9]+)?)\.\s+(.+)$", stripped)
            if m_sec:
                num = persian_to_ascii_digits(m_sec.group(1))
                title = process_inline(m_sec.group(2))
                self.in_section_2_13 = num == "2-13"
                self.out.append(f"\\section{{{title}}}")
                self.i += 1
                continue

            m_sub = re.match(r"^###\s+(.+)$", stripped)
            if m_sub:
                title = process_inline(m_sub.group(1))
                self.out.append(f"\\subsection{{{title}}}")
                self.i += 1
                continue

            m_subsub = re.match(r"^####\s+(.+)$", stripped)
            if m_subsub:
                title = process_inline(m_subsub.group(1))
                self.out.append(f"\\subsubsection{{{title}}}")
                self.i += 1
                continue

            # Skip chapter titles
            if re.match(r"^#\s+فصل\s+", stripped):
                self.i += 1
                continue

            # Skip appendix / bibliography sections from expanded markdown
            if re.match(r"^#\s+پیوست\s+", stripped) or stripped == "# منابع":
                break

            # Display math
            if stripped.startswith("$$"):
                math_lines = []
                if stripped.endswith("$$") and len(stripped) > 4:
                    math_lines.append(stripped[2:-2].strip())
                    self.i += 1
                else:
                    self.i += 1
                    while self.i < len(self.lines):
                        l = self.lines[self.i].strip()
                        if l.endswith("$$"):
                            math_lines.append(l[:-2].strip())
                            self.i += 1
                            break
                        math_lines.append(l)
                        self.i += 1
                math_body = "\n".join(line for line in math_lines if line.strip())
                self.out.append("\\begin{latin}")
                self.out.append("\\[")
                self.out.append(math_body)
                self.out.append("\\]")
                self.out.append("\\end{latin}")
                continue

            # Code block
            if stripped.startswith("```"):
                lang = stripped[3:].strip()
                self.i += 1
                code_lines = []
                while self.i < len(self.lines) and not self.lines[self.i].strip().startswith("```"):
                    code_lines.append(self.lines[self.i])
                    self.i += 1
                self.i += 1  # skip closing ```
                self.out.append("\\begin{latin}")
                self.out.append("\\begin{lstlisting}[basicstyle=\\ttfamily\\footnotesize]")
                self.out.extend(code_lines)
                self.out.append("\\end{lstlisting}")
                self.out.append("\\end{latin}")
                continue

            # Image
            m_img = re.match(r"^!\[(.+?)\]\((.+?)\)$", stripped)
            if m_img:
                alt, src = m_img.group(1), m_img.group(2)
                basename = Path(src).name
                if basename == "taxonomy_blockchain_scaling.png":
                    self.out.append(SPECIAL_TAXONOMY_FIG)
                else:
                    img_file, label = IMAGE_MAP.get(basename, (basename, f"fig:{basename[:-4]}"))
                    self.out.append(figure_latex(alt, img_file, label))
                self.i += 1
                continue

            # Table caption marker
            if stripped.startswith("**جدول") and stripped.endswith("**"):
                cap = stripped.strip("*")
                self.pending_caption = process_inline(cap)
                self.i += 1
                continue

            # Table 2-1 special replacement
            if self.in_section_2_13 and self.pending_caption and "۲-۱" in self.pending_caption.replace("2-1", "۲-۱"):
                if stripped.startswith("|"):
                    # skip entire markdown table
                    while self.i < len(self.lines) and self.lines[self.i].strip().startswith("|"):
                        self.i += 1
                    self.out.append(SPECIAL_TABLE_2_1)
                    self.pending_caption = None
                    continue

            # Markdown table
            if stripped.startswith("|"):
                header = parse_table_row(stripped)
                self.i += 1
                sep = parse_table_row(self.lines[self.i].strip()) if self.i < len(self.lines) else []
                self.i += 1
                aligns = col_alignments(sep) if sep else ["l"] * len(header)
                rows = []
                while self.i < len(self.lines) and self.lines[self.i].strip().startswith("|"):
                    rows.append(parse_table_row(self.lines[self.i].strip()))
                    self.i += 1
                cap = self.pending_caption or "جدول"
                self.pending_caption = None
                self.out.append("\\begin{table}[h]")
                self.out.append("\\centering")
                self.out.append(f"\\caption{{{cap}}}")
                self.out.append("\\small")
                self.out.append(build_tabular(header, rows, aligns))
                self.out.append("\\end{table}")
                continue

            # Unordered list
            if re.match(r"^[-*]\s+", stripped):
                self.out.append("\\begin{itemize}")
                while self.i < len(self.lines):
                    l = self.lines[self.i].strip()
                    m = re.match(r"^[-*]\s+(.+)$", l)
                    if not m:
                        break
                    self.out.append(f"\\item {process_inline(m.group(1))}")
                    self.i += 1
                self.out.append("\\end{itemize}")
                continue

            # Ordered list
            if re.match(r"^[۰-۹0-9]+\.\s+", stripped):
                self.out.append("\\begin{enumerate}")
                while self.i < len(self.lines):
                    l = self.lines[self.i].strip()
                    m = re.match(r"^[۰-۹0-9]+\.\s+(.+)$", l)
                    if not m:
                        break
                    self.out.append(f"\\item {process_inline(m.group(1))}")
                    self.i += 1
                self.out.append("\\end{enumerate}")
                continue

            # Horizontal rule
            if stripped in ("---", "***", "___"):
                self.i += 1
                continue

            # Regular paragraph
            self.out.append(process_inline(stripped))
            self.pending_caption = None
            self.i += 1

        return "\n".join(self.out) + "\n"


def extract_chapters(md: str) -> dict[str, str]:
    lines = md.splitlines()
    markers = []
    for idx, line in enumerate(lines):
        if re.match(r"^#\s+فصل\s+", line.strip()):
            markers.append((idx, line.strip()))

    def slice_chapter(start_idx: int, end_idx: int | None) -> str:
        chunk = lines[start_idx:end_idx]
        # drop first line (chapter title)
        if chunk and re.match(r"^#\s+فصل\s+", chunk[0].strip()):
            chunk = chunk[1:]
        # stop before appendices / references in chapter 5
        trimmed = []
        for ln in chunk:
            if re.match(r"^#\s+پیوست\s+", ln.strip()) or ln.strip() == "# منابع":
                break
            trimmed.append(ln)
        return "\n".join(trimmed)

    chapters = {}
    for i, (idx, title) in enumerate(markers):
        end = markers[i + 1][0] if i + 1 < len(markers) else len(lines)
        key = persian_to_ascii_digits(title)
        if "اول" in title or "1" in key:
            chapters["ch1"] = slice_chapter(idx, end)
        elif "دوم" in title or "2" in key:
            ch2 = slice_chapter(idx, end)
            # split at section 2-13
            split_pat = re.compile(r"^##\s+۲-۱۳\.\s+")
            split_idx = None
            for j, ln in enumerate(ch2.splitlines()):
                if split_pat.match(ln.strip()) or re.match(r"^##\s+2-13\.\s+", ln.strip()):
                    split_idx = j
                    break
            if split_idx is None:
                chapters["ch2-1"] = ch2
                chapters["ch2-2"] = ""
            else:
                ch2_lines = ch2.splitlines()
                chapters["ch2-1"] = "\n".join(ch2_lines[:split_idx])
                chapters["ch2-2"] = "\n".join(ch2_lines[split_idx:])
        elif "سوم" in title:
            chapters["ch3"] = slice_chapter(idx, end)
        elif "چهارم" in title:
            chapters["ch4"] = slice_chapter(idx, end)
        elif "پنجم" in title:
            chapters["ch5"] = slice_chapter(idx, end)
    return chapters


def write_chapter(path: Path, header: str, body: str):
    conv = Converter(body)
    latex_body = conv.convert()
    content = header + "\n" + latex_body
    path.write_text(content, encoding="utf-8")
    print(f"Wrote {path} ({len(latex_body.splitlines())} lines body)")


def main():
    md = MD_PATH.read_text(encoding="utf-8")
    chapters = extract_chapters(md)

    write_chapter(
        OUT_DIR / "chapter1.tex",
        "% !TeX root=main.tex\n"
        "% دستور زیر باعث شماره‌بندی صفحات فصول از ۱ می‌شود و باید در اولین فصل شما باشد. آن را حذف نکنید!\n"
        "\\pagenumbering{arabic} % 1, 2, ...\n\n"
        "\\chapter{مقدمه}",
        chapters.get("ch1", ""),
    )

    write_chapter(
        OUT_DIR / "chapter2-1.tex",
        "% !TeX root=main.tex\n\\chapter{مروری بر مطالعات انجام شده}",
        chapters.get("ch2-1", ""),
    )

    write_chapter(
        OUT_DIR / "chapter2-2.tex",
        "% !TeX root=main.tex",
        chapters.get("ch2-2", ""),
    )

    write_chapter(
        OUT_DIR / "chapter_architecture.tex",
        "% !TeX root=main.tex\n\\chapter{معماری سیستم بلاکچین پیشنهادی}",
        chapters.get("ch3", ""),
    )

    write_chapter(
        OUT_DIR / "chapter_results.tex",
        "% !TeX root=main.tex\n\\chapter{نتایج آزمایشات و ارزیابی عملکرد}",
        chapters.get("ch4", ""),
    )

    write_chapter(
        OUT_DIR / "chapter_conclusion.tex",
        "% !TeX root=main.tex\n\\chapter{نتیجه‌گیری و کارهای آینده}",
        chapters.get("ch5", ""),
    )


if __name__ == "__main__":
    main()
