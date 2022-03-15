import logging
from multiprocessing import Process

import numpy as np

from src.app import db
from src.models import *

MAX_PROCESS_COUNT = 12


def extract_documents_text(id_range):
    logging.info("Started documents text extraction from %d to %d", id_range[0], id_range[-1])
    print(f"Started documents text extraction from {id_range[0]} to {id_range[-1]}")
    for document in NoticeDocument.query.filter(NoticeDocument.id.in_(id_range.tolist())).all():
        print(f"Extracting text for document #{document.id}")
        if document.extracted_text is None:
            print(f"\textracting {document}")
            document.extract_text()
            db.session.commit()
        else:
            print(f"\tSKIPPING: {document}")
    # db.session.commit()
    # db.session.close()
    logging.info("Finished documents text extraction from %d to %d", id_range[0], id_range[-1])


def run_multiprocess_extract_documents_text():
    logging.info("Started multiprocessing documents text extraction")
    # pool = Pool(processes=4)
    # pool.map(extract_documents_text, range(0, NoticeDocument.query.count(), 100))

    processes = []
    id_range_array = np.array(range(NoticeDocument.query.count() - 1))
    for c, rng in enumerate(np.array_split(id_range_array, MAX_PROCESS_COUNT)):
        print(f"Creating process #{c} for range: {rng[0]} to {rng[-1]}")
        p = Process(target=extract_documents_text, args=([rng]))
        processes.append(p)

    # return

    for c, p in enumerate(processes):
        print(f"Starting process #{c}")
        p.start()

    for c, p in enumerate(processes):
        print(f"Joining process #{c}")
        p.join()
        print(f"Joined process #{c}")

    logging.info("Finished multiprocessing documents text extraction")


if __name__ == "__main__":
    run_multiprocess_extract_documents_text()
