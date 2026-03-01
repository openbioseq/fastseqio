---
icon: lucide/dna
---

# fastseqio

`fastseqio` is a Python library for fast reading and writing of FASTA/FASTQ files.
It supports plain text and gzip-compressed files (`.gz`) and provides a small, practical API centered on:

- `seqioFile`: file reader/writer
- `Record`: sequence record object

---

## Installation

```bash
pip install fastseqio
```

---

## Quick Start

### Read records (FASTA/FASTQ auto-detection)

```python
from fastseqio import seqioFile

with seqioFile("test-data/test2.fa", "r") as f:
    for record in f:
        print(record.name, record.sequence)
```

### Write FASTA

```python
from fastseqio import seqioFile

with seqioFile("out.fa", "w") as f:
    f.writeFasta("seq1", "ACGGGGGGGTTTT")
    f.writeFasta("seq2", "TTTTCCCCAAAAG")
```

### Write FASTQ

```python
from fastseqio import seqioFile

with seqioFile("out.fq", "w") as f:
    f.writeFastq("read1", "ACGT", "IIII")
```

---

## Features

- **Automatic format detection**: Reads both FASTA and FASTQ files seamlessly
- **Gzip support**: Transparent reading/writing of `.gz` compressed files
- **Streaming support**: Use `"-"` as file path for stdin/stdout
- **Efficient iteration**: Low memory footprint with sequential reading
- **Rich sequence operations**: Homopolymer compression, k‑mer generation, reverse, subseq, case conversion
- **Flexible writing**: Configurable line width, comment inclusion, base case

---

## Documentation Overview

- **[API Reference](api/seqiofile.md)**: Complete documentation for `seqioFile`
- **[Record API](api/record.md)**: Complete documentation for `Record`
- **[Examples](examples.md)**: Practical usage examples
- **[Advanced Usage](advanced.md)**: Gzip, write options, and performance tips

---

## License

MIT License. See [LICENSE](https://github.com/dwpeng/fastseqio/blob/main/LICENSE) for details.

---

## Source Code

The project is hosted on GitHub: [dwpeng/fastseqio](https://github.com/dwpeng/fastseqio)