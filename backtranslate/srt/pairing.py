def pair_by_index(chinese_list, english_list):
    """Pair by sequential index. Stops at the shorter list length."""
    pairs = []
    for i in range(min(len(chinese_list), len(english_list))):
        pairs.append((chinese_list[i], english_list[i]))
    return pairs


def pair_by_timecode(chinese_list, english_list):
    """Pair subtitles with overlapping time ranges."""
    pairs = []

    ci = 0
    ei = 0
    while ci < len(chinese_list) and ei < len(english_list):
        ch = chinese_list[ci]
        en = english_list[ei]

        overlap_start = max(ch["start"], en["start"])
        overlap_end = min(ch["end"], en["end"])

        if overlap_start < overlap_end:
            pairs.append((ch, en))
            ci += 1
            ei += 1
        elif ch["start"] < en["start"]:
            ci += 1
        else:
            ei += 1

    return pairs
