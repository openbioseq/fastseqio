---
icon: lucide/file-text
---

# seqioFile

The `seqioFile` class provides reading and writing of FASTA/FASTQ files, with automatic format detection and gzip support.

## Constructor

```python
seqioFile(
    path: str,
    mode: Literal["r", "w"] = "r",
    compressed: bool = False,
)
```

Opens a FASTA/FASTQ file for reading or writing.

**Parameters**

- `path` (`str`): File path. Use `"-"` for stdin (read mode) or stdout (write mode).
- `mode` (`"r"` | `"w"`): `"r"` for reading, `"w"` for writing. Default `"r"`.
- `compressed` (`bool`): Force gzip compression. If `path` ends with `.gz`, compression is automatically enabled.

**Raises**

- `ValueError`: If `mode` is not `"r"` or `"w"`.

**Notes**

- If `path` ends with `.gz`, the file is treated as gzip-compressed regardless of the `compressed` argument.
- In read mode, the file format (FASTA/FASTQ) is automatically detected per record.
- The file handle should be closed via `.close()` or preferably used as a context manager (`with seqioFile(...) as f`).

**Examples**

```python
# Read a plain text FASTA/FASTQ file
reader = seqioFile("data.fa", "r")

# Write a gzipped FASTA file (automatic detection via .gz extension)
writer = seqioFile("output.fa.gz", "w")

# Read from stdin
import sys
reader = seqioFile("-", "r")
```

---

## Read Methods

All read methods return a [`Record`](record.md) object, or `None` at end-of-file.

### `readOne()`

```python
readOne() -> Optional[Record]
```

Reads the next record, auto-detecting FASTA/FASTQ format.

**Returns**

- `Record` or `None`: The next record, or `None` if EOF.

**Raises**

- `ValueError`: If file not opened in read mode.

**Example**

```python
with seqioFile("data.fq", "r") as f:
    while (rec := f.readOne()) is not None:
        print(rec.name)
```

### `readFasta()`

```python
readFasta() -> Optional[Record]
```

Reads the next FASTA record (skips FASTQ records).

**Returns**

- `Record` or `None`: The next FASTA record, or `None` if EOF.

**Raises**

- `ValueError`: If file not opened in read mode.

### `readFastq()`

```python
readFastq() -> Optional[Record]
```

Reads the next FASTQ record (skips FASTA records).

**Returns**

- `Record` or `None`: The next FASTQ record, or `None` if EOF.

**Raises**

- `ValueError`: If file not opened in read mode.

---

## Write Methods

### `writeOne()`

```python
writeOne(
    name: str,
    sequence: str,
    quality: Optional[str] = None,
    comment: Optional[str] = None,
) -> None
```

Writes a single record in FASTA (if `quality` is `None`) or FASTQ format.

**Parameters**

- `name` (`str`): Sequence identifier.
- `sequence` (`str`): Nucleotide sequence.
- `quality` (`Optional[str]`): Quality scores (required for FASTQ).
- `comment` (`Optional[str]`): Optional comment line (after `name`).

**Raises**

- `ValueError`: If file not opened in write mode.
- `AssertionError`: If `quality` is provided but `len(quality) != len(sequence)`.

**Example**

```python
with seqioFile("out.fa", "w") as f:
    f.writeOne("seq1", "ACGT", comment="example")

with seqioFile("out.fq", "w") as f:
    f.writeOne("read1", "ACGT", "IIII")
```

### `writeFasta()`

```python
writeFasta(name: str, sequence: str, comment: Optional[str] = None) -> None
```

Convenience wrapper for `writeOne(name, sequence, comment=comment)`.

### `writeFastq()`

```python
writeFastq(
    name: str,
    sequence: str,
    quality: str,
    comment: Optional[str] = None,
) -> None
```

Convenience wrapper for `writeOne(name, sequence, quality, comment=comment)`.

### `writeRecord()`

```python
writeRecord(record: Record, fastq: bool = False) -> None
```

Writes an existing `Record` object.

**Parameters**

- `record` (`Record`): The record to write.
- `fastq` (`bool`): If `True`, write as FASTQ (requires `record.quality`). Default `False` (FASTA).

**Raises**

- `ValueError`: If file not opened in write mode.
- `AssertionError`: If `fastq=True` and `len(record.sequence) != len(record.quality)`.

---

## Writer Configuration

### `set_write_options()`

```python
set_write_options(
    *,
    lineWidth: Optional[int] = None,
    includeComments: Optional[bool] = None,
    baseCase: Optional[Literal["upper", "lower"]] = None,
) -> None
```

Adjusts formatting of written records.

**Parameters**

- `lineWidth` (`Optional[int]`): Wrap sequence lines to this width (must be > 0). Default `None` (no wrapping).
- `includeComments` (`Optional[bool]`): Whether to write comment lines (FASTA `>` header comment). Default `None` (keep current).
- `baseCase` (`Optional["upper" | "lower"]`): Convert sequence letters to uppercase or lowercase. Default `None` (keep original).

**Raises**

- `ValueError`: If file not opened in write mode.
- `AssertionError`: If `lineWidth <= 0`.

**Example**

```python
with seqioFile("out.fa", "w") as f:
    f.set_write_options(lineWidth=60, baseCase="upper")
    f.writeFasta("seq", "acgtacgt")
```

---

## Properties

### `readable` → `bool`
`True` if file opened in read mode.

### `writable` → `bool`
`True` if file opened in write mode.

### `size` → `int`
File size in bytes (read mode only).

### `offset` → `int`
Current byte offset within the file (read mode only).

---

## Utility Methods

### `reset()`
Rewinds the file to the beginning (read mode only). Allows re‑reading the same file.

### `fflush()`
Flushes any buffered data to disk (write mode only).

### `close()`
Closes the file handle. Called automatically when exiting a `with` block.

### `__iter__()`
Enables iteration over records: `for record in file: ...`.

**Example**

```python
with seqioFile("data.fa", "r") as f:
    for rec in f:
        print(rec.name, rec.sequence)
```

---

## Context Manager

`seqioFile` supports the context‑manager protocol for automatic closing:

```python
with seqioFile("data.fa", "r") as f:
    records = list(f)
```