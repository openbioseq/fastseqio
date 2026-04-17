import os
import tempfile
from fastseqio import seqioFile, Record


def test_read():
    file = seqioFile("test-data/test2.fa")

    records = []
    for record in file:
        records.append(record)

    assert len(records) == 3

    assert records[0].name == "a"
    assert records[1].name == "b"
    assert records[2].name == "c"

    records = []
    for record in file:
        records.append(record)

    assert len(records) == 0

    file.reset()

    records = []
    for record in file:
        records.append(record)

    assert len(records) == 3


def test_write():

    with seqioFile("out.fa", "w") as file:
        file.writeFasta("test", "ACGGGGGGGTTTT")
        file.writeFasta("test", "ACGGGGGGGTTTT")

    content = ">test\nACGGGGGGGTTTT\n>test\nACGGGGGGGTTTT\n"

    with open("out.fa", "r") as fp:
        data = fp.read()
        assert data == content

    os.remove("out.fa")


def test_write_gz():
    # compress by extension or let `compressed=True`
    file = seqioFile("out.fa.gz", "w")

    file.writeFasta("test", "ACGGGGGGGTTTT")
    file.writeFasta("test", "ACGGGGGGGTTTT")

    file.close()
    import gzip

    content = ">test\nACGGGGGGGTTTT\n>test\nACGGGGGGGTTTT\n"

    with open("out.fa.gz", "rb") as fp:
        data = fp.read()
        data = gzip.decompress(data).decode("utf-8")
        assert data == content

    os.remove("out.fa.gz")


def test_record():
    record = Record("test", "ACGGGGGGGTTTT")

    assert record.name == "test"
    assert record.sequence == "ACGGGGGGGTTTT"

    record.name = "test2"
    record.sequence = "ACGGGGGGGTTTTTTTT"

    assert record.name == "test2"
    assert record.sequence == "ACGGGGGGGTTTTTTTT"

    hpc = record.hpc()
    assert hpc == "ACGT"

    rev = record.reverse()
    assert rev == "TTTTTTTTGGGGGGGCA"

    length = record.length
    assert length == 17

    length = len(record)
    assert length == 17

    record.sequence += "xxx"
    assert record.length == 20
    assert record.sequence == "ACGGGGGGGTTTTTTTTxxx"
    assert len(record) == 20

    record.sequence = "ACGGGGGGGTTTT"

    sub = record.subseq(2, 5)
    assert sub == "GGGGG"


def test_kmers():
    record = Record("test", "ACGGGG")

    kmers = list(record.kmers(4))
    assert len(kmers) == (len(record) - 4 + 1)
    assert kmers == ["ACGG", "CGGG", "GGGG"]


def test_pickle():
    import pickle

    record = Record("test", "ACGGGG")

    obj = pickle.dumps(record)

    record = pickle.loads(obj)

    assert record.name == "test"
    assert record.sequence == "ACGGGG"


def test_seqiofile_size_offset():
    file = seqioFile("test-data/test2.fa")
    fp = open("test-data/test2.fa", "r")
    filesize = os.path.getsize("test-data/test2.fa")
    records = []
    for record in file:
        records.append(record)
        print(file.offset)

    print(records)

    assert file.size == filesize

    fp.read()

    assert file.offset == fp.tell()


def mock_fastq():
    _, tmp_path = tempfile.mkstemp(suffix=".fastq")
    with open(tmp_path, "w") as fp:
        fp.write("@a c1\n")
        fp.write("AAAAAAAAAAAAA\n")
        fp.write("+\n")
        fp.write("IIIIIIIIIIIII\n")

        fp.write("@b      \n")
        fp.write("GGGGGGGGGGGGG\n")
        fp.write("+\n")
        fp.write("JJJJJ@JJJJJJJ\n")

        fp.write("@c\n")
        fp.write("CCCCCCCCCCCC\n")
        fp.write("+\n")
        fp.write("@@@@KKKKKKKC\n")

    return tmp_path


def test_read_fastq():

    fastq_path = mock_fastq()

    file = seqioFile(fastq_path)
    records = []
    for record in file:
        records.append(record)

    for record in records:
        print(record.name, record.sequence, record.quality)

    assert len(records) == 3
    assert records[0].name == "a"
    assert records[0].comment == "c1"
    assert records[0].sequence == "AAAAAAAAAAAAA"
    assert records[0].quality == "IIIIIIIIIIIII"
    assert records[1].name == "b"
    assert records[1].comment is None
    assert records[1].sequence == "GGGGGGGGGGGGG"
    assert records[1].quality == "JJJJJ@JJJJJJJ"
    assert records[2].name == "c"
    assert records[2].comment is None
    assert records[2].sequence == "CCCCCCCCCCCC"
    assert records[2].quality == "@@@@KKKKKKKC"

    os.remove(fastq_path)


def mock_fasta():
    _, tmp_path = tempfile.mkstemp(suffix=".fa")
    with open(tmp_path, "w") as fp:
        fp.write(">a   \n")
        fp.write("ACGGGGGGGTTTT\n")
        fp.write("AAAAAAAAAAAAA\n")

        fp.write(">b cb\n")
        fp.write("ACGGGGGGGTTTT\n")

        fp.write(">c c ccc cccc\n")
        fp.write("ACGGGGGGGTTTT\n")

    return tmp_path


def test_read_fasta():

    fasta_path = mock_fasta()

    file = seqioFile(fasta_path)
    records = []
    for record in file:
        records.append(record)

    assert len(records) == 3
    assert records[0].name == "a"
    assert records[0].comment is None
    assert records[0].sequence == "ACGGGGGGGTTTTAAAAAAAAAAAAA"
    assert records[1].name == "b"
    assert records[1].comment == "cb"
    assert records[1].sequence == "ACGGGGGGGTTTT"
    assert records[2].name == "c"
    assert records[2].comment == "c ccc cccc"
    assert records[2].sequence == "ACGGGGGGGTTTT"

    os.remove(fasta_path)
