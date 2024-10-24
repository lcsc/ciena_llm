from common import ClimateImpactExtractorTest

TEST_NAME = "news-elpais-binary-5T-2F"
DATASET_DIR = "news-elpais-binary"
DATASET_PATH = (
    f"/home/javier/Developer/SeqIA/data/test-datasets-small/{TEST_NAME}/sample"
)


test = ClimateImpactExtractorTest(TEST_NAME, DATASET_DIR, DATASET_PATH)
test.run()
