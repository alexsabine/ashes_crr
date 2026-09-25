"""Coverage audit (Lossless_Pause/DECLARATION_2.md): what the dossiers of 2026-09-23 to 2026-09-25 cover, by count of distinct arXiv ids and
their year (from the id's YYMM prefix). Non-arXiv sources (docs, blogs, proceedings) are counted by their section headers
only where a dossier marks them. Run: python3 Lossless_Pause/checks/coverage.py
"""
import glob
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
GROUPS = [('energy (prompt 199)', 'docs/citations/energy_*_2026-09-25.md'),
          ('compute scale (prompt 198)', 'docs/citations/compute_scale_2026-09-25.md'),
          ('lossless pause (prompt 202)', 'docs/citations/lossless_pause_*_2026-09-25.md'),
          ('continual-learning SOTA (prompt 191)', 'docs/citations/cl_sota_*_2026-09-25.md'),
          ('CL frontier (prompts 105, 179, 190)', 'docs/citations/frontier_*cl*_2026-09-2*.md'),
          ('plasticity and FOREVER', 'docs/citations/*plasticity*_2026-09-2*.md'),
          ('safety and pause (earlier days)', 'docs/citations/*safety*_2026-09-2*.md'),
          ('empty-cut engineering (prompt 154)', 'docs/citations/empty_cut_engineering_2026-09-24.md'),
          ('systematic sweep (prompt 203)', 'docs/citations/sweep_*_2026-09-25.md')]
ID = re.compile(r'(?<![\d.])(\d{2})(\d{2})\.(\d{4,5})(?:v\d+)?(?![\d])')


def main():
    print('Coverage audit of the dossiers fetched 2026-09-23 to 2026-09-25 (distinct arXiv ids; year from the id prefix)')
    tot = set()
    for label, pat in GROUPS:
        files = sorted(glob.glob(os.path.join(ROOT, pat)))
        ids = set()
        for f in files:
            for yy, mm, n in ID.findall(open(f, encoding='utf-8').read()):
                if 1 <= int(mm) <= 12 and 7 <= int(yy) <= 26:
                    ids.add(f'{yy}{mm}.{n}')
        tot |= ids
        by = {}
        for i in ids:
            y = 2000 + int(i[:2])
            by[y] = by.get(y, 0) + 1
        recent = sum(v for y, v in by.items() if y >= 2024)
        print(f'  {label:38} files {len(files):2d}  arXiv ids {len(ids):4d}  of which 2024-2026 {recent:4d}  '
              f"2026 {by.get(2026, 0):3d}  by year {dict(sorted(by.items()))}")
    print(f'  all groups: {len(tot)} distinct arXiv ids')


if __name__ == '__main__':
    main()
