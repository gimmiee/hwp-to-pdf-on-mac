# hwp-to-pdf-on-mac

**한국어 · English** — 이 README는 두 언어로 작성되어 있습니다.

- [한국어](#한국어)
- [English](#english)

---

## 한국어

맥(macOS)에서 **HWP / HWPX** 파일을 **PDF**로 일괄 변환하는 CLI 도구입니다.

한컴오피스·Polaris Office 없이, 로컬에 있는 HWP 파일을 PDF로 일괄 정리할 때 사용합니다.

## 특징

- **맥 네이티브** — Windows 한/글이나 Polaris 없이 동작
- **일괄 변환** — 폴더 안 HWP/HWPX를 한 번에 처리 (하위 폴더 포함)
- **원본 보존** — HWP는 그대로 두고, PDF만 별도 폴더에 저장
- **다른 파일 무시** — PDF, DOCX, JPG 등은 건드리지 않음
- **재실행 안전** — 이미 변환된 PDF는 건너뜀 (`--force`로 덮어쓰기 가능)

## 요구 사항

- macOS (Apple Silicon / Intel)
- Python **3.10+**
- (선택) [pnpm](https://pnpm.io/) — `package.json` 스크립트 사용 시

## 설치

```bash
git clone https://github.com/gimmiee/hwp-to-pdf-on-mac.git
cd hwp-to-pdf-on-mac
```

### 방법 A — pnpm (권장)

```bash
pnpm bootstrap
```

가상환경(`.venv`) 생성 + 의존성 설치까지 한 번에 진행합니다.

### 방법 B — Python만

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 사용법

### 기본

```bash
pnpm convert -- "/path/to/HWP폴더"
```

또는:

```bash
source .venv/bin/activate
python3 convert.py "/path/to/HWP폴더"
```

### 예시

```bash
# 폴더 일괄 변환
pnpm convert -- "~/Documents/hwp-files"

# 출력 위치 직접 지정
pnpm convert -- "~/Documents/hwp-files" -o "~/Documents/pdf-output"

# 이미 만든 PDF 다시 생성
pnpm convert -- "~/Documents/hwp-files" --force

# 현재 폴더만 (하위 폴더 제외)
pnpm convert -- "~/Documents/hwp-files" --no-recursive
```

Finder에서 폴더를 터미널로 **끌어다 놓으면** 경로 입력이 편합니다.

```bash
pnpm convert -- ␣   # 여기서 폴더를 터미널에 드래그 후 Enter
```

## 결과는 어디에 저장되나요?

**입력 폴더 안이 아니라, 옆에 `-pdf`가 붙은 새 폴더**에 저장됩니다.

| 입력 | 출력 (기본) |
|------|-------------|
| `…/my-documents` | `…/my-documents-pdf` |
| `…/my-documents/reports/file.hwp` | `…/my-documents-pdf/reports/file.pdf` |

하위 폴더 구조는 그대로 유지됩니다.  
입력 폴더 최상단에 PDF·DOCX만 있고 HWP가 하위 폴더에만 있다면, 변환된 PDF도 `-pdf` 폴더의 **같은 하위 경로**에 생깁니다.

변환에 실패한 파일은 출력 폴더의 `failed.txt`에 기록됩니다.

## 옵션

| 옵션 | 설명 |
|------|------|
| `input` | HWP 파일이 들어 있는 폴더 (필수) |
| `-o`, `--output` | PDF 저장 폴더 (미지정 시 `<입력폴더명>-pdf`) |
| `-r`, `--recursive` | 하위 폴더까지 변환 (기본값) |
| `--no-recursive` | 현재 폴더의 파일만 변환 |
| `--skip-existing` | 이미 있는 PDF 건너뛰기 (기본값) |
| `--force` | 기존 PDF 덮어쓰기 |

## 지원 형식·제한

| 항목 | 내용 |
|------|------|
| 입력 | `.hwp`, `.hwpx` |
| 출력 | `.pdf` |
| 호환성 | 일반 문서·과제·보고서 수준에서 실용적. 표·수식·복잡한 레이아웃은 원본과 다를 수 있음 |
| 권장 | 변환 후 샘플 몇 개를 열어 레이아웃 확인 |

## 프로젝트 구조

```
hwp-to-pdf-on-mac/
├── convert.py          # 변환 CLI
├── requirements.txt    # rhwp-python
├── package.json        # pnpm 스크립트
└── README.md
```

## 기술 스택

변환 엔진은 [rhwp-python](https://pypi.org/project/rhwp-python/) (Rust 기반 [rhwp](https://github.com/edwardkim/rhwp) 바인딩)을 사용합니다.

- HWP / HWPX 동시 지원
- macOS arm64 / x64 wheel 제공

## 라이선스

이 저장소의 스크립트: **MIT** (자유롭게 사용·수정 가능)

변환 엔진 `rhwp-python`: [MIT](https://pypi.org/project/rhwp-python/)

## 기여

이슈·PR 환영합니다. 버그 리포트 시 OS 버전, Python 버전, 실패한 HWP 종류(가능하면 `failed.txt` 내용)를 함께 적어 주시면 도움이 됩니다.

---

## English

**Korean · English** — This README is available in two languages. See [한국어](#한국어) above.

Batch-convert **HWP / HWPX** files to **PDF** on **macOS** from the command line.

Useful when you need to batch-convert local HWP files to PDF without Hancom Office or a Polaris Office subscription.

### Features

- **Native on Mac** — no Windows Hangul or Polaris required
- **Batch conversion** — processes all `.hwp` / `.hwpx` in a folder (including subfolders)
- **Preserves originals** — HWP files stay untouched; PDFs go to a separate folder
- **Ignores other files** — PDF, DOCX, JPG, etc. are skipped
- **Safe to re-run** — skips existing PDFs unless you pass `--force`

### Requirements

- macOS (Apple Silicon or Intel)
- Python **3.10+**
- (Optional) [pnpm](https://pnpm.io/) — for `package.json` scripts

### Setup

```bash
git clone https://github.com/gimmiee/hwp-to-pdf-on-mac.git
cd hwp-to-pdf-on-mac
pnpm bootstrap
```

Or with Python only:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Usage

```bash
pnpm convert -- "/path/to/your-hwp-folder"
```

Or:

```bash
source .venv/bin/activate
python3 convert.py "/path/to/your-hwp-folder"
```

Examples:

```bash
pnpm convert -- "~/Documents/hwp-files"
pnpm convert -- "~/Documents/hwp-files" -o "~/Documents/pdf-output"
pnpm convert -- "~/Documents/hwp-files" --force
pnpm convert -- "~/Documents/hwp-files" --no-recursive
```

Drag a folder from Finder into the terminal to paste its path easily.

### Where are PDFs saved?

PDFs are **not** written into the input folder. By default, a **sibling folder** named `<input-folder-name>-pdf` is created next to it.

| Input | Default output |
|-------|----------------|
| `…/my-documents` | `…/my-documents-pdf` |
| `…/my-documents/reports/file.hwp` | `…/my-documents-pdf/reports/file.pdf` |

Subfolder structure is mirrored under the `-pdf` folder. If HWP files live only in subfolders, look inside `-pdf` at the same paths—not at the top level of the original folder.

Failed conversions are logged to `failed.txt` in the output folder.

### Options

| Option | Description |
|--------|-------------|
| `input` | Folder containing HWP files (required) |
| `-o`, `--output` | Output folder (default: `<input-name>-pdf`) |
| `-r`, `--recursive` | Include subfolders (default) |
| `--no-recursive` | Only files in the top-level folder |
| `--skip-existing` | Skip if PDF already exists (default) |
| `--force` | Overwrite existing PDFs |

### Formats & limitations

| | |
|---|---|
| Input | `.hwp`, `.hwpx` |
| Output | `.pdf` |
| Fidelity | Good for typical documents; tables, equations, and complex layouts may differ from the original |
| Tip | Open a few sample PDFs after conversion to verify layout |

### Tech stack

Uses [rhwp-python](https://pypi.org/project/rhwp-python/) (Rust [rhwp](https://github.com/edwardkim/rhwp) bindings): HWP + HWPX support, macOS arm64 / x64 wheels.

### License

Scripts in this repo: **MIT**. Conversion engine `rhwp-python`: [MIT](https://pypi.org/project/rhwp-python/).

### Contributing

Issues and PRs welcome. For bugs, please include macOS version, Python version, and `failed.txt` if available.
