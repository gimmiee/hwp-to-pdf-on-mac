#!/usr/bin/env python3
"""HWP/HWPX → PDF 일괄 변환 (개인용)."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

from rhwp import Document

HWP_EXTENSIONS = {".hwp", ".hwpx"}


def find_documents(root: Path, recursive: bool) -> list[Path]:
    if recursive:
        files = [p for p in root.rglob("*") if p.is_file()]
    else:
        files = [p for p in root.iterdir() if p.is_file()]

    return sorted(
        p
        for p in files
        if p.suffix.lower() in HWP_EXTENSIONS and not p.name.startswith(".")
    )


def output_path_for(input_file: Path, input_root: Path, output_root: Path) -> Path:
    relative = input_file.relative_to(input_root)
    return output_root / relative.with_suffix(".pdf")


def convert_file(input_file: Path, pdf_path: Path) -> None:
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    doc = Document(str(input_file))
    doc.export_pdf(str(pdf_path))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="HWP/HWPX 파일을 PDF로 일괄 변환합니다.",
    )
    parser.add_argument(
        "input",
        type=Path,
        help="HWP 파일이 들어 있는 폴더",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="PDF 저장 폴더 (기본: 입력폴더 옆에 <폴더명>-pdf)",
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        default=True,
        help="하위 폴더까지 변환 (기본: 켜짐)",
    )
    parser.add_argument(
        "--no-recursive",
        action="store_false",
        dest="recursive",
        help="현재 폴더만 변환",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        default=True,
        help="이미 있는 PDF는 건너뜀 (기본: 켜짐)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="기존 PDF도 덮어쓰기",
    )
    args = parser.parse_args()

    input_root = args.input.expanduser().resolve()
    if not input_root.is_dir():
        print(f"오류: 입력 폴더를 찾을 수 없습니다 — {input_root}", file=sys.stderr)
        return 1

    output_root = (
        args.output.expanduser().resolve()
        if args.output
        else input_root.parent / f"{input_root.name}-pdf"
    )
    output_root.mkdir(parents=True, exist_ok=True)

    skip_existing = args.skip_existing and not args.force
    documents = find_documents(input_root, args.recursive)

    if not documents:
        print(f"변환할 HWP/HWPX 파일이 없습니다: {input_root}")
        return 0

    failed_log = output_root / "failed.txt"
    failed_lines: list[str] = []
    ok = 0
    skipped = 0
    failed = 0

    print(f"입력: {input_root}")
    print(f"출력: {output_root}")
    print(f"대상: {len(documents)}개 파일")
    print("—" * 50)

    for i, input_file in enumerate(documents, start=1):
        pdf_path = output_path_for(input_file, input_root, output_root)
        label = f"[{i}/{len(documents)}] {input_file.name}"

        if skip_existing and pdf_path.exists():
            if pdf_path.stat().st_mtime >= input_file.stat().st_mtime:
                print(f"건너뜀 {label}")
                skipped += 1
                continue

        try:
            convert_file(input_file, pdf_path)
            print(f"완료   {label} → {pdf_path.relative_to(output_root)}")
            ok += 1
        except Exception as exc:  # noqa: BLE001 — 사용자 로그용
            msg = f"{input_file}\t{exc}"
            failed_lines.append(msg)
            print(f"실패   {label}: {exc}", file=sys.stderr)
            failed += 1

    print("—" * 50)
    print(f"성공 {ok} · 건너뜀 {skipped} · 실패 {failed}")

    if failed_lines:
        header = (
            f"# 변환 실패 목록 ({datetime.now(timezone.utc).isoformat()})\n"
            f"# 입력: {input_root}\n"
        )
        failed_log.write_text(header + "\n".join(failed_lines) + "\n", encoding="utf-8")
        print(f"실패 목록: {failed_log}")
        return 1

    if failed_log.exists():
        failed_log.unlink()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
