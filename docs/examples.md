---
icon: lucide/beaker
---

# Examples

Practical usage examples for `fastseqio`.

## Basic Reading

### Read all records from a file

```python
from fastseqio import seqioFile

with seqioFile("data.fa", "r") as f:
    for record in f:
        print(record.name, record.sequence[:10], "...")
```

### Read specific format

If you know the file contains only FASTA or only FASTQ, you can use the dedicated methods:

```python
with seqioFile("data.fa", "r") as f:
    while (rec := f.readFasta()) is not None:
        print(rec.name)
```

### Read with manual iteration

```python
f = seqioFile("data.fq", "r")
try:
    while True:
        rec = f.readOne()
        if rec is None:
            break
        process(rec)
finally:
    f.close()
```

---

## Basic Writing

### Write a FASTA file

```python
from fastseqio import seqioFile

with seqioFile("output.fa", "w") as f:
    f.writeFasta("seq1", "ACGTACGT", comment="first sequence")
    f.writeFasta("seq2", "TTTTCCCCAAAAG")
```

### Write a FASTQ file

```python
with seqioFile("output.fq", "w") as f:
    f.writeFastq("read1", "ACGT", "IIII")
    f.writeFastq("read2", "GCTA", "JJJJ", comment="high quality")
```

### Write using `writeOne`

```python
with seqioFile("mixed.fq", "w") as f:
    # FASTA (no quality)
    f.writeOne("seq1", "ACGT")
    # FASTQ (with quality)
    f.writeOne("read1", "ACGT", "IIII")
```

---

## Working with Records

### Create and modify records

```python
from fastseqio import Record

rec = Record("original", "ACGTacgt", comment="mixed case")
print(rec.upper())          # "ACGTACGT"
print(rec.hpc())            # "ACGTacgt" (no compression here)

rec.sequence = "AAAATTTT"
print(rec.hpc())            # "AT"

rec.reverse(inplace=True)
print(rec.sequence)         # "TTTTAAAA"
```

### Extract k‑mers

```python
rec = Record("test", "ACGTACGT")
for k in [2, 3, 4]:
    print(f"{k}-mers:", list(rec.kmers(k)))
# Output:
# 2-mers: ['AC', 'CG', 'GT', 'TA', 'AC', 'CG', 'GT']
# 3-mers: ['ACG', 'CGT', 'GTA', 'TAC', 'ACG', 'CGT']
# 4-mers: ['ACGT', 'CGTA', 'GTAC', 'TACG']
```

### Subsequence extraction

```python
rec = Record("long", "ACGTTGCA" * 10)
# Using subseq
middle = rec.subseq(20, 10)
# Using slice notation
middle = rec[20:30]
```

---

## Gzip Compression

### Reading gzipped files

```python
# Automatic detection via .gz extension
with seqioFile("reads.fa.gz", "r") as f:
    for rec in f:
        print(rec.name)

# Force gzip mode (e.g., when reading from stdin)
import sys
with seqioFile("-", "r", compressed=True) as f:
    data = list(f)
```

### Writing gzipped files

```python
# Automatic via extension
with seqioFile("output.fa.gz", "w") as f:
    f.writeFasta("seq1", "ACGT")

# Explicit compression flag
with seqioFile("output.fa", "w", compressed=True) as f:
    f.writeFasta("seq2", "TGCA")  # still writes compressed data
```

---

## Writer Configuration

### Line wrapping and case conversion

```python
with seqioFile("formatted.fa", "w") as f:
    f.set_write_options(lineWidth=60, baseCase="upper")
    f.writeFasta("long", "ACGT" * 100)
```

### Include/exclude comments

```python
with seqioFile("with_comments.fa", "w") as f:
    f.set_write_options(includeComments=True)
    f.writeFasta("seq1", "ACGT", comment="has comment")

with seqioFile("no_comments.fa", "w") as f:
    f.set_write_options(includeComments=False)
    f.writeFasta("seq2", "ACGT", comment="ignored")
```

---

## Streaming (stdin/stdout)

### Read from stdin

```bash
cat data.fa | python -c "
from fastseqio import seqioFile
import sys
with seqioFile('-', 'r') as f:
    for rec in f:
        sys.stdout.write(rec.name + '\n')
"
```

### Write to stdout

```python
import sys
with seqioFile("-", "w") as f:
    f.writeFasta("stdout_seq", "ACGT")
# Output appears on stdout
```

---

## Real‑World Pipeline Example

Process a FASTQ file, filter by length, convert to uppercase, write FASTA:

```python
from fastseqio import seqioFile

with seqioFile("input.fq", "r") as fin, \
     seqioFile("output.fa", "w") as fout:

    fout.set_write_options(baseCase="upper")

    for rec in fin:
        if len(rec) >= 50:
            rec.upper(inplace=True)
            fout.writeRecord(rec)   # writes as FASTA (no quality)
```

---

## Error Handling

### Validate quality lengths

```python
from fastseqio import seqioFile

try:
    with seqioFile("broken.fq", "w") as f:
        f.writeFastq("bad", "ACGT", "III")  # length mismatch
except AssertionError as e:
    print("Quality length error:", e)
```

### Check file modes

```python
f = seqioFile("data.fa", "r")
print(f.readable)   # True
print(f.writable)   # False
```