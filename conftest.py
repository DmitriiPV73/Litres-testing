import pytest
from selenium import webdriver

@pytest.fixture(scope="function")
def browser():
    chrom = webdriver.Chrome()
    chrom.maximize_window()
    chrom.implicitly_wait(10)
    yield chrom
    chrom.quit()



