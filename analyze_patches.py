#!/usr/bin/env python3

import os
import unidiff
import sys
import chardet
import argparse
import whatthepatch
import mailbox
import csv

def strip_prefix(s):
    if s.startswith('a/') or s.startswith('b/'):
        return s[2:]
    return s

def pick_file_name(old_path, new_path):
    if old_path == '/dev/null':
        return new_path.strip()
    if new_path == '/dev/null':
        return old_path.strip()
    return old_path.strip()

def fallback_get_files(patch_data):
    files = []
    for line in patch_data.splitlines():
        if line.startswith('diff --git'):
            old_path_start = line.find(' a/')
            new_path_start = line.find(' b/')
            if old_path_start == -1:
                old_path = '/dev/null'
            else:
                old_path = line[old_path_start+3:new_path_start]

            if new_path_start == -1:
                new_path = '/dev/null'
            else:
                new_path = line[new_path_start+3:]
            files.append(pick_file_name(old_path, new_path))
    return files

def count_modified_lines_unidiff(patchset : unidiff.PatchSet):
    added = 0
    removed = 0
    for patch in patchset:
        for hunk in patch:
            added += hunk.added
            removed += hunk.removed
    return added, removed

def count_modified_lines_whatthepatch(patchset):
    added = 0
    removed = 0
    for diff in patchset:
        if diff.changes is None:
            continue
        for change in diff.changes:
            if isinstance(change.line, bytes):
                # skip binary files
                continue
            if change.old is None:
                added += 1
            elif change.new is None:
                removed += 1
            else:
                # unchanged
                pass
    return added, removed

def count_modified_lines_fallback(patch_data):
    added = 0
    removed = 0
    for line in patch_data.splitlines():
        if line.startswith('+') and not line.startswith('+++'):
            added += 1
        elif line.startswith('-') and not line.startswith('---'):
            removed += 1
    return added, removed

def handle_patch(commit, data):
    # remove everything before the first diff
    data = data[data.find(b'diff --git'):]
    detected = chardet.detect(data)
    if detected['encoding'] is None:
        detected['encoding'] = 'latin1'
    try:
        patchset_u = unidiff.PatchSet(data.decode(detected['encoding']))
        patchset_w = list(whatthepatch.parse_patch(data.decode(detected['encoding'])))
        files_u = [x.path for x in patchset_u]
        files_w = [pick_file_name(x.header.old_path, x.header.new_path) for x in patchset_w]
        files_f = fallback_get_files(data.decode(detected['encoding']))
        assert files_u == files_w
        assert files_u == files_f
        assert files_w == files_f
        added, removed = count_modified_lines_unidiff(patchset_u)
        added2, removed2 = count_modified_lines_whatthepatch(patchset_w)
        added3, removed3 = count_modified_lines_fallback(data.decode(detected['encoding']))
        # if added != added2 or removed != removed2:
        #     print(added, removed, file=sys.stderr)
        #     print(added2, removed2, file=sys.stderr)
        #     print(count_modified_lines_fallback(data.decode(detected['encoding'])), file=sys.stderr)

    except AssertionError as e:
        print(commit)
        # print(added, added2)
        # print(removed, removed2)
        print(files_u)
        print(files_w)
        print(files_f)
        print(set(files_u) - set(files_f))
        print(set(files_f) - set(files_u))
        raise e
    except TypeError as e:
        print(commit, e)
        print(detected)
        raise e
    return files_u, added, removed

def main():
    parser = argparse.ArgumentParser(description='Analyze patches')
    parser.add_argument('files', metavar='file', type=str, nargs='+',
                        help='patch files')
    args = parser.parse_args()

    writer = csv.writer(sys.stdout)
    writer.writerow(['commit', 'files', 'added', 'removed'])

    for file in args.files:
        commit = os.path.basename(file.replace('.patch', ''))
        data = open(file, 'rb').read()
        if data.startswith(b'From '):
            # mbox format
            mbox = mailbox.mbox(file)
            fileset = set()
            added_lines = 0
            removed_lines = 0
            for message in mbox:
                # Throw away headers
                sub_data = message.get_payload(decode=True)
                files, lines_added, lines_removed = handle_patch(commit, sub_data)
                fileset |= set(files)
                added_lines += lines_added
                removed_lines += lines_removed
            writer.writerow([commit, len(fileset), added_lines, removed_lines])
        else:
            files, lines_added, lines_removed = handle_patch(commit, data)
            writer.writerow([commit, len(files), lines_added, lines_removed])


if __name__ == "__main__":
    main()
