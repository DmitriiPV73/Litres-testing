import pytest
from selenium import webdriver

@pytest.fixture(scope="function")
def browser(request):
    """Фикстура принимает параметр от parametrize"""
    b = request.param
    if b == 'Chrome':
        chrom = webdriver.Chrome()
        chrom.maximize_window()
        chrom.implicitly_wait(10)
        yield chrom
        chrom.quit()
    elif b == 'Firefox':
        firefox = webdriver.Firefox()
        firefox.maximize_window()
        firefox.implicitly_wait(10)
        yield firefox
        firefox.quit()



