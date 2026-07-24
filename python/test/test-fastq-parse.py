from fastseqio import seqioFile


def test_read():
    file = seqioFile("test-data/large.fq.gz")
    nrecords = 0
    for record in file:
        nrecords += 1
        if len(record) != len(record.sequence) or len(record) != len(record.quality):
            print(
                f"Record length: {len(record)}, Sequence length: {len(record.sequence)}, Quality length: {len(record.quality)}"
            )
            print(f"{record.sequence}")
            print(f"{record.quality}")
        assert len(record) == len(record.sequence) == len(record.quality)

    assert nrecords == 398


if __name__ == "__main__":
    test_read()
