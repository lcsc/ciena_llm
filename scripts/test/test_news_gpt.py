from common import ClimateImpactExtractorTest

TEST_NAME = "news-gpt-drought-news-article-generator"
DATASET_DIR = TEST_NAME
DATASET_PATH = f"/home/javier/Developer/SeqIA/data/{DATASET_DIR}/sample"

test = ClimateImpactExtractorTest(TEST_NAME, DATASET_DIR, DATASET_PATH)
test.run()
