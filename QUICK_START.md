# 🚀 Quick Start - آخرین مرحله!

## یک بسته نهایی مانده: `tocloft`

همه چیز آماده است. فقط یک بسته دیگر نیاز است.

### گزینه 1: اجرای خودکار (توصیه می‌شود)

```bash
./build_thesis.sh
```

این دستور:
1. بسته `tocloft` را نصب می‌کند (رمز عبور می‌خواهد)
2. پایان‌نامه را کامپایل می‌کند
3. PDF را باز می‌کند

###  گزینه 2: نصب دستی

اگر اسکریپت کار نکرد، این دستورات را اجرا کنید:

```bash
# 1. نصب bسته آخر
export PATH="/usr/local/texlive/2025basic/bin/universal-darwin:$PATH"
sudo tlmgr install tocloft

# 2. کامپایل
cd thesis_latex_sample
xelatex -interaction=nonstopmode main.tex
bibtex main
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
open main.pdf
```

## 📊 وضعیت نصب

✅ **نصب شده**:
- framed, lastpage
- todonotes
- algorithm2e, algorithms
- tabulary, tabularx
- adjustbox, subfigure
- pgf, tikz
- glossaries
- xepersian
- و 10 بسته دیگر...

⏳ **باقی‌مانده**:
- `tocloft` ← فقط این یکی!

## 🎯 بعد از نصب

PDF شما در این مسیر خواهد بود:
```
thesis_latex_sample/main.pdf
```

موفق باشید! 🎓

