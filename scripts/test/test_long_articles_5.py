from common import ClimateImpactExtractorTest

TEST_NAME = "test-jvela-long-articles-5"
DATASET_DIR = "test-datasets-small"
DATASET_PATH = f"/home/javier/Developer/SeqIA/data/{DATASET_DIR}/{TEST_NAME}/sample"

test = ClimateImpactExtractorTest(TEST_NAME, DATASET_DIR, DATASET_PATH)
test.run()
