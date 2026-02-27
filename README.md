# fastseqio (Python)

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

## File API (`seqioFile`)

### Create a file handle

```python
seqioFile(path: str, mode: "r" | "w" = "r", compressed: bool = False)
```

- `path`: input/output file path. Use `"-"` for stdin/stdout.
- `mode`:
  - `"r"`: read mode
  - `"w"`: write mode
- `compressed`: force gzip mode when needed (for example when `path="-"`).

Notes:
- If `path` ends with `.gz`, compression is enabled automatically.
- Iteration consumes the file. Use `reset()` to read again.

### Read methods

- `readOne()` → read next record (auto format)
- `readFasta()` → read next FASTA record
- `readFastq()` → read next FASTQ record
- `for record in file:` → iterate with `readOne()` internally

All read methods return `Record` or `None` at end-of-file.

### Write methods

- `writeFasta(name, sequence, comment=None)`
- `writeFastq(name, sequence, quality, comment=None)`
- `writeOne(name, sequence, quality=None, comment=None)`
  - writes FASTA when `quality` is not provided
  - writes FASTQ when `quality` is provided
- `writeRecord(record, fastq=False)`

Validation:
- For FASTQ, sequence length must equal quality length.

### Writer options

```python
file.set_write_options(
    lineWidth=80,            # optional, > 0
    includeComments=True,    # optional
    baseCase="upper",       # optional: "upper" or "lower"
)
```

### Utilities and properties

- `reset()` → rewind file to beginning
- `fflush()` → flush write buffer
- `close()` → close file
- `readable` / `writable`
- `size` → file size in bytes
- `offset` → current byte offset

---

## Record API (`Record`)

### Create a record

```python
from fastseqio import Record

record = Record("seq1", "ACGGGG", quality=None, comment="example")
```

### Fields

- `record.name`
- `record.sequence`
- `record.quality`
- `record.comment`
- `record.length` (same as `len(record)`)

### Sequence helpers

- `record.upper(inplace=False)`
- `record.lower(inplace=False)`
- `record.reverse(inplace=False)`
- `record.subseq(start, length)`
- `record.hpc()` (homopolymer compression)
- `record.kmers(k)` (iterator of k-mers)

Example:

```python
from fastseqio import Record

r = Record("id", "AAACCCGGGTTT")
print(r.hpc())            # ACGT
print(list(r.kmers(4)))   # ['AAAC', 'AACC', ...]
```

---

## Gzip Example

```python
from fastseqio import seqioFile

# Compression auto-detected by .gz suffix
with seqioFile("reads.fa.gz", "w") as w:
    w.writeFasta("seq1", "ACGTACGT")

with seqioFile("reads.fa.gz", "r") as r:
    for rec in r:
        print(rec.name)
```

---

## Recommended Usage Pattern

Use context managers (`with seqioFile(...) as f`) so files are always closed correctly.
