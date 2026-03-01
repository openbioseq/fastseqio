---
icon: lucide/book-open-text
---

# Record

The `Record` class represents a single FASTA/FASTQ sequence record with name, sequence, quality, and comment fields.

## Constructor

```python
Record(
    name: str,
    sequence: str,
    quality: Optional[str] = None,
    comment: Optional[str] = None,
)
```

Creates a new sequence record.

**Parameters**

- `name` (`str`): Sequence identifier (the part after `>` or `@`).
- `sequence` (`str`): Nucleotide sequence.
- `quality` (`Optional[str]`): Quality scores (for FASTQ records). Default `None`.
- `comment` (`Optional[str]`): Optional comment (the part after the identifier on the same line). Default `None`.

**Examples**

```python
# FASTA record
fa = Record("seq1", "ACGTACGT", comment="example")

# FASTQ record
fq = Record("read1", "ACGT", "IIII")
```

---

## Attributes

All attributes are gettable and settable.

### `name` → `str`
Sequence identifier.

### `sequence` → `str`
Nucleotide sequence.

### `quality` → `str`
Quality scores (empty string for FASTA records).

### `comment` → `Optional[str]`
Comment line (without the leading space). `None` if absent.

### `length` → `int`
Length of the sequence (same as `len(record)`).

---

## Sequence Operations

### `upper(inplace=False)`

```python
upper(inplace: bool = False) -> str
```

Returns the sequence converted to uppercase.

**Parameters**

- `inplace` (`bool`): If `True`, modifies the record’s sequence in place. Default `False`.

**Returns**

- `str`: Uppercase sequence.

**Example**

```python
rec = Record("id", "acgt")
print(rec.upper())          # "ACGT"
print(rec.sequence)         # "acgt"
rec.upper(inplace=True)
print(rec.sequence)         # "ACGT"
```

### `lower(inplace=False)`

```python
lower(inplace: bool = False) -> str
```

Returns the sequence converted to lowercase.

**Parameters**

- `inplace` (`bool`): If `True`, modifies the record’s sequence in place. Default `False`.

**Returns**

- `str`: Lowercase sequence.

### `reverse(inplace=False)`

```python
reverse(inplace: bool = False) -> str
```

Returns the reverse of the sequence.

**Parameters**

- `inplace` (`bool`): If `True`, reverses the record’s sequence in place. Default `False`.

**Returns**

- `str`: Reversed sequence.

**Example**

```python
rec = Record("id", "ACGT")
print(rec.reverse())        # "TGCA"
```

### `hpc()`

```python
hpc() -> str
```

Homopolymer compression: removes consecutive identical bases.

**Returns**

- `str`: Compressed sequence.

**Example**

```python
rec = Record("id", "AAATTTCCCGGG")
print(rec.hpc())            # "ATCG"
```

### `subseq(start, length)`

```python
subseq(start: int, length: int) -> str
```

Extracts a subsequence.

**Parameters**

- `start` (`int`): Start index (0‑based).
- `length` (`int`): Number of bases to extract.

**Returns**

- `str`: Subsequence.

**Raises**

- `AssertionError`: If `start` or `start + length` are out of bounds.

**Example**

```python
rec = Record("id", "ACGTACGT")
print(rec.subseq(2, 4))     # "GTAC"
```

### `kmers(k)`

```python
kmers(k: int) -> Iterator[str]
```

Generates all k‑mers of length `k` from the sequence.

**Parameters**

- `k` (`int`): K‑mer length.

**Yields**

- `str`: Next k‑mer.

**Raises**

- `ValueError`: If `k > len(record)`.

**Example**

```python
rec = Record("id", "ACGT")
for kmer in rec.kmers(2):
    print(kmer)             # "AC", "CG", "GT"
```

---

## Slicing

Records support slice notation to extract subsequences:

```python
rec = Record("id", "ACGTACGT")
print(rec[2:6])             # "GTAC"
```

Internally uses `__gititem__` (note the typo in the current implementation). The slice must be contiguous; step is not supported.

---

## Magic Methods

### `__len__()`
Returns sequence length. Equivalent to `record.length`.

### `__str__()`
Returns a short representation: `"seqioRecord(name=...)"`.

### `__repr__()`
Returns a developer‑friendly representation: `"seqioRecord(name=..., len=...)"`.

---

## Internal Notes

- The `Record` class wraps a low‑level `_seqioRecord` C++ object.
- The `_fromRecord` class method is used internally by `seqioFile` to construct Python records from C++ objects.
- Quality strings are stored as empty strings for FASTA records; the `quality` property returns `""`, not `None`.

---

## Pickling Support

`Record` instances can be serialized with `pickle`:

```python
import pickle
rec = Record("id", "ACGT")
data = pickle.dumps(rec)
rec2 = pickle.loads(data)
```