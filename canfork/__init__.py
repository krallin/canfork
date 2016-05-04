# -*- coding: utf-8 -*-
import re

__author__ = 'Thomas Orozco'
__email__ = 'thomas@orozco.fr'
__version__ = '0.2.0'


KERN_INFO_LINE_REGEXP = re.compile(r"([\w()]+):\W+(.+)")


class KernInfoParseException(Exception):
    pass


def normalize_raw_kerninfo(raw_kerninfo):
    out = {}

    for k, v in raw_kerninfo.items():
        if "kB" in v:
            v = int(v.split(' ', 1)[0])
        elif k == "VmFlags":
            v = set(f for f in v.split(' ') if f)
        out[k] = v

    return out


def parse_memory_map(f):
    raw_vmas = []

    curr_raw_vma = None
    for line in f:
        m = KERN_INFO_LINE_REGEXP.match(line)

        # New VM Area.
        if m is None:
            # Handle the VMA we were processing if any.
            if curr_raw_vma is not None:
                raw_vmas.append(curr_raw_vma)
            curr_raw_vma = {}
            continue

        # Unexpected: we found a k / v before seeing any VMA.
        if curr_raw_vma is None:
            err = "Encountered line {0} before finding new VMA!".format(line)
            raise KernInfoParseException(err)

        # Update the VMA with the new key.
        k, v = m.groups()
        curr_raw_vma[k] = v

    return [normalize_raw_kerninfo(raw_vma) for raw_vma in raw_vmas]


def parse_meminfo(f):
    raw_meminfo = {}
    for line in f:
        m = KERN_INFO_LINE_REGEXP.match(line)
        if m is None:
            err = "Encountered invalid line {0} in meminfo!".format(line)
            raise KernInfoParseException(err)

        k, v = m.groups()
        raw_meminfo[k] = v

    return normalize_raw_kerninfo(raw_meminfo)


def max_accounted_vma_size(vmas):
    # Don't include VMAs that aren't accounted for
    accounted_vma_sizes = [vma["Size"] for vma in vmas
                           if "ac" in vma["VmFlags"]]
    if not accounted_vma_sizes:
        return 0
    return max(accounted_vma_sizes)


def main():
    import sys
    import mmap

    if len(sys.argv) != 2:
        print("usage: {0} PID".format(sys.argv[0]))
        sys.exit(2)

    with open("/proc/{0}/smaps".format(sys.argv[1])) as f:
        vmas = parse_memory_map(f)

    with open("/proc/meminfo") as f:
        meminfo = parse_meminfo(f)

    max_vma = max_accounted_vma_size(vmas)
    mem_free = meminfo["MemFree"]

    # Print basic memory stats for the process and system.
    print("MaxVma:\t{0} kB".format(max_vma))
    print("MemFree:\t{0} kB".format(mem_free))

    # While MemFree vs. MaxVma is a good estimate of whether we can fork, in
    # practice it might not be 100% accurate or reflect actual allocation
    # space. So, let's try to allocate some memory and see if it works. We
    # won't actually use any of that memory, so this will just allocate some
    # virtual memory but should not trigger e.g. the OOM killer.
    for alloc_pct in range(100, 201, 10):
        alloc_size_kb = int(max_vma * float(alloc_pct) / 100)
        try:
            m = mmap.mmap(-1, alloc_size_kb * 1024,
                          mmap.MAP_PRIVATE | mmap.MAP_ANONYMOUS,
                          mmap.PROT_READ | mmap.PROT_WRITE)
            m.close()
        except mmap.error:
            alloc_state = "KO"
        else:
            alloc_state = "OK"
        print("Alloc{0}:\t{1}".format(alloc_pct, alloc_state))

    ret = int(max_vma > mem_free)
    print("Status:\t{0}".format(ret))
    sys.exit(ret)


if __name__ == "__main__":
    main()
