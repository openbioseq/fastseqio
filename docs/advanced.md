---
icon: lucide/settings
---

# Advanced Usage

Tips, performance considerations, and edge cases for `fastseqio`.

## Performance Tips

### Iteration vs. `readOne`

The fastest way to read a whole file is using the iterator:

```python
with seqioFile("large.fa", "r") as f:
    for record in f:
        process(record)
```

This avoids Python‑level function call overhead. Use `readOne` only when you need to conditionally stop reading.

### Re‑reading with `reset`

If you need to traverse the same file multiple times, call `reset()` instead of reopening:

```python
f = seqioFile("data.fa", "r")
first_pass = list(f)
f.reset()
second_pass = list(f)
f.close()
```

### Batch Processing

For very large files, process records in batches to limit memory:

```python
batch = []
with seqioFile("huge.fa", "r") as f:
    for rec in f:
        batch.append(rec)
        if len(batch) >= 10000:
            process_batch(batch)
            batch.clear()
    if batch:
        process_batch(batch)
```

---

## Memory and File Handles

### Always close files

Use context managers (`with`) whenever possible. If you cannot, ensure `close()` is called:

```python
f = seqioFile("data.fa", "r")
try:
    # work with f
finally:
    f.close()
```

### File size and offset

The `size` and `offset` properties are only available in read mode. They reflect the underlying file descriptor’s position, which may be ahead of the last delivered record due to buffering.

---

## Gzip Details

### Compression detection

- If the path ends with `.gz`, gzip mode is activated automatically.
- If you pipe a gzip stream to stdin (`path="-"`), you must set `compressed=True`.
- Writing with `compressed=True` but without a `.gz` extension still produces gzip‑compressed data (the file will not be recognized by `gunzip` unless you rename it).

### Performance trade‑offs

Gzip decompression is single‑threaded and can become the bottleneck for very large files. Consider uncompressed files for intermediate storage in pipelines.

---

## Writer Options Deep Dive

### Line wrapping

Line wrapping only affects the sequence part, not the header or quality lines.

```python
with seqioFile("wrapped.fa", "w") as f:
    f.set_write_options(lineWidth=10)
    f.writeFasta("seq", "ACGT" * 5)
# Output:
# >seq
# ACGTACGTAC
# GTACGTACGT
```

Setting `lineWidth` to `None` (default) writes the entire sequence on one line.

### Base case conversion

Base case conversion is applied before line wrapping. If you need case‑sensitive operations later, convert in Python with `record.upper(inplace=True)` instead.

### Comment inclusion

Comments are only written if `includeComments=True` **and** the record’s `comment` field is non‑empty. FASTA headers are written as `>name comment` (space added automatically). FASTQ headers are `@name comment`.

---

## FASTQ Quality Encoding

`fastseqio` does not validate quality score encoding (Sanger, Illumina 1.8+, etc.). It treats quality as an opaque string. Ensure your quality strings match the expected encoding of downstream tools.

### Quality length enforcement

When writing FASTQ, the library asserts that `len(sequence) == len(quality)`. This check is performed in Python, not in C++, so it can be disabled by running Python with `-O` (optimize mode). Do not rely on it for production validation.

---

## stdin/stdout quirks

### Reading from stdin

- `seqioFile("-", "r")` reads from `sys.stdin.buffer`.
- The file must be seekable for `reset()` to work; `reset()` will raise an error on stdin.
- Use `compressed=True` if stdin is gzip‑compressed.

### Writing to stdout

- `seqioFile("-", "w")` writes to `sys.stdout.buffer`.
- Buffering may cause output to appear only after `close()` or `fflush()`.
- On Windows, binary mode is automatically used for stdout.

---

## Thread Safety

`seqioFile` objects are **not** thread‑safe. Concurrent calls to `readOne` or `writeOne` from multiple threads may corrupt internal state.

If you need parallel processing, read the file sequentially and distribute records to worker threads (or processes). Each worker should have its own `seqioFile` instance for writing.

---

## Platform‑Specific Notes

### Windows

- File paths can be relative or absolute; use forward slashes or double backslashes.
- Gzip support works the same as on Unix.
- Stdio in binary mode is handled transparently.

### macOS / Linux

No special considerations.

---

## Debugging

### Enable assertions

The library uses `assert` statements for many preconditions (quality length, write mode, etc.). Run Python with `-O` to disable them, but only after you have verified your code works correctly.

### Check file modes

If a method raises `ValueError` with "File not opened in read/write mode", verify the `mode` argument passed to the constructor.

### Inspect internal state

The `_raw()` method returns the underlying C++ object (for debugging only):

```python
rec = Record("test", "ACGT")
raw = rec._raw()
print(type(raw))   # <class '_fastseqio.seqioRecord'>
```

---

## Known Limitations

1. **No support for multi‑line FASTQ quality strings**: The FASTQ format requires quality scores to be on a single line; `fastseqio` does not split or join quality lines.
2. **No validation of sequence alphabet**: Letters other than `ACGTN` are allowed.
3. **No support for paired‑end reads**: Each record is independent.
4. **No support for custom record separators**: Only standard FASTA/FASTQ formats are recognized.

---

## Getting Help

If you encounter unexpected behavior, please open an issue on GitHub with:

- The version of `fastseqio` (`pip show fastseqio`)
- A minimal reproducible example
- The actual and expected output