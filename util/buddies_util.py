

def find_buddy(buddies, name, multiple=False):
    found = [fr["name"].lower().find(name) for fr in buddies]
    found = [_idx for _idx, el in enumerate(found) if el >= 0]

    if found:
        if not multiple and len(found) > 1:
            print("Multiple matches found, returning first...")

        return buddies[found[0]] if not multiple else [buddies[f] for f in found]

    return None
