from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import tempfile
import sys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

inputstring=sys.argv[1]

dir_out=tempfile.TemporaryDirectory()

#print (dir_out.name)

fxProfile = FirefoxProfile()

fxProfile.set_preference("browser.download.folderList",2)
fxProfile.set_preference("browser.download.manager.showWhenStarting",False)
fxProfile.set_preference("browser.download.dir",dir_out.name)
fxProfile.set_preference("browser.helperApps.neverAsk.saveToDisk","image/png")

opts = Options()
opts.set_headless()
assert opts.headless  # Operating in headless mode
geckoPath = './geckodriver'
browser = Firefox(firefox_profile=fxProfile,executable_path=geckoPath,options=opts)
browser.get('https://regexper.com/')
search_form = browser.find_element_by_id('regexp-input')
search_form.send_keys(inputstring)
search_form.submit()
links = browser.find_elements_by_class_name('inline-icon')
#print(len(links))
for link in links:
    #print(link.get_attribute("data-action"))
    if(link.get_attribute("data-action")=='download-png'):
        #print(link.get_attribute("href"))
        WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[starts-with(@data-action, 'download-png')]"))).click()
        link.click()
browser.close()
browser.quit()
fh= open(dir_out.name+'/image.png', 'rb')
ba = bytearray(fh.read())
sys.stdout.buffer.write(ba)
#print(dir_out.name+'/image.png')


