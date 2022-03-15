import math
import os
from argparse import ArgumentParser
from collections import namedtuple
from concurrent.futures import ProcessPoolExecutor

import editdistance

WorkerResult = namedtuple('WorkerResult', ['num_errors', 'num_words'])

def process(
        transcripts,
        references,
        indices) -> WorkerResult:

    error_count = 0
    word_count = 0

    for i in indices:
        tr, ref = transcripts[i], references[i]

        ref_words = ref.lower().split()
        words = tr.lower().split()

        error_count += editdistance.eval(ref_words, words)
        word_count += len(ref_words)

    return WorkerResult(num_errors=error_count, num_words=word_count)


def main():
    parser = ArgumentParser()
    parser.add_argument('--transcript', required=True)
    parser.add_argument('--reference', required=True)
    parser.add_argument('--num-workers', type=int, default=os.cpu_count())
    args = parser.parse_args()

    # read
    transcripts = []
    references = []
    with open(args.transcript) as f:
        for line in f:
            transcripts.append(line.rstrip())
    with open(args.reference) as f:
        for line in f:
            references.append(line.rstrip())

    assert len(transcripts) == len(references), 'len(transcripts) and len(references) differ.'

    indices = list(range(len(transcripts)))

    num_workers = args.num_workers
    chunk = math.ceil(len(indices) / num_workers)

    futures = list()
    with ProcessPoolExecutor(num_workers) as executor:
        for i in range(num_workers):

            future = executor.submit(
                process,
                transcripts=transcripts,
                references=references,
                indices=indices[i * chunk: (i + 1) * chunk]
            )
            futures.append(future)

    res = [x.result() for x in futures]

    num_errors = sum(x.num_errors for x in res)
    num_words = sum(x.num_words for x in res)

    print(f'WER: {(100 * float(num_errors) / num_words):.2f}')

if __name__ == '__main__':
    main()
