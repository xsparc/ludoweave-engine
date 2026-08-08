#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 || ! -d "$1" ]]; then
  echo "expected release directory is unavailable" >&2
  exit 1
fi
if [[ "$GITHUB_REPOSITORY" != "xsparc/ludoweave-engine" ]]; then
  echo "unexpected release repository" >&2
  exit 1
fi
if [[ ! "$RELEASE_ID" =~ ^[1-9][0-9]{0,18}$ ]]; then
  echo "invalid public release id" >&2
  exit 1
fi
if [[ ${#RELEASE_ID} -eq 19 && "$RELEASE_ID" > "9223372036854775807" ]]; then
  echo "invalid public release id" >&2
  exit 1
fi

expected_dir="$1"
plan="$RUNNER_TEMP/release-assets.plan"
use_existing_plan=false
if [[ $# -eq 2 ]]; then
  if [[ "$2" != "--use-existing-plan" || ! -f "$plan" ]]; then
    echo "existing release plan is unavailable" >&2
    exit 1
  fi
  use_existing_plan=true
else
  test ! -e "$plan"
fi
public_document="$RUNNER_TEMP/release-public.json"
public_dir="$RUNNER_TEMP/release-public-download"
verify_expected_release() {
  python scripts/verify_release_draft.py \
    "$expected_dir" "$public_document" \
    --expected-tag "$GITHUB_REF_NAME" --expected-title "$RELEASE_TITLE" \
    --expected-state published "$@"
}
test ! -e "$public_document"
test ! -e "$public_dir"
mkdir "$public_dir"
curl --disable --fail --silent --show-error --location --max-redirs 3 \
  --connect-timeout 10 --max-time 30 \
  --proto '=https' --proto-redir '=https' \
  --header "Accept: application/vnd.github+json" \
  --header "X-GitHub-Api-Version: 2026-03-10" \
  "https://api.github.com/repos/$GITHUB_REPOSITORY/releases/$RELEASE_ID" \
  | head -c 4194305 > "$public_document"
test "$(wc -c < "$public_document")" -le 4194304
if [[ "$use_existing_plan" == true ]]; then
  verify_expected_release
else
  verify_expected_release --asset-plan "$plan"
fi
exec 3< "$plan"
IFS= read -r protocol <&3
test "$protocol" = "ludoweave.release-asset-retrieval-plan/1"
asset_count=0
expected_total=0
while IFS=$'\t' read -r asset_id expected_bytes asset_name <&3; do
  if [[ ! "$asset_id" =~ ^[1-9][0-9]{0,18}$ ]]; then
    echo "invalid release asset id" >&2
    exit 1
  fi
  if [[ ${#asset_id} -eq 19 && "$asset_id" > "9223372036854775807" ]]; then
    echo "invalid release asset id" >&2
    exit 1
  fi
  if [[ ! "$expected_bytes" =~ ^(0|[1-9][0-9]{0,8})$ ]]; then
    echo "invalid release asset size" >&2
    exit 1
  fi
  if [[ ${#expected_bytes} -eq 9 && "$expected_bytes" > "268435456" ]]; then
    echo "invalid release asset size" >&2
    exit 1
  fi
  if [[ ! "$asset_name" =~ ^[0-9A-Za-z][0-9A-Za-z._+-]{0,255}$ ]]; then
    echo "invalid release asset name" >&2
    exit 1
  fi
  test "$asset_count" -lt 32
  expected_total=$((expected_total + expected_bytes))
  test "$expected_total" -le 536870912
  target="$public_dir/$asset_name"
  partial="$public_dir/.asset-$asset_id.part"
  test ! -e "$target"
  test ! -e "$partial"
  curl --disable --fail --silent --show-error --location --max-redirs 3 \
    --connect-timeout 10 --max-time 30 \
    --proto '=https' --proto-redir '=https' \
    --header "Accept: application/octet-stream" \
    --header "X-GitHub-Api-Version: 2026-03-10" \
    "https://api.github.com/repos/$GITHUB_REPOSITORY/releases/assets/$asset_id" \
    | head -c "$((expected_bytes + 1))" > "$partial"
  test "$(wc -c < "$partial")" -eq "$expected_bytes"
  mv "$partial" "$target"
  asset_count=$((asset_count + 1))
done
exec 3<&-
test "$asset_count" -gt 0
python scripts/verify_release_draft.py \
  "$public_dir" "$public_document" \
  --expected-tag "$GITHUB_REF_NAME" --expected-title "$RELEASE_TITLE" \
  --expected-state published
python scripts/smoke_release.py "$public_dir"
