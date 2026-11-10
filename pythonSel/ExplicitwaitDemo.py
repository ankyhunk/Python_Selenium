from selenium import webdriver

#chrome driver
from selenium.webdriver.chrome.service import Service
#-- Chrome
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
#['Cucumber - 1 Kg', 'Raspberry - 1/4 Kg', 'Strawberry - 1/4 Kg']

#service_obj = Service()
service_obj = Service()
driver = webdriver.Chrome(service=service_obj)
driver.implicitly_wait(2)
# 5 seconds is max time out.. 2 seconds (3 seconds save)
driver.get("https://rahulshettyacademy.com/seleniumPractise/#/")
driver.find_element(By.CSS_SELECTOR,".search-keyword").send_keys("ber")
wait = WebDriverWait(driver, 10, ignored_exceptions=[StaleElementReferenceException])
wait.until(lambda d: (names := d.find_elements(By.CSS_SELECTOR, "div.products h4.product-name"))
           and all("ber" in n.text.lower() for n in names))

results = driver.find_elements(By.XPATH, "//div[@class='products']/div")#list[]
count = len(results)
assert count > 0
for result in results:
    result.find_element(By.XPATH,"div/button").click()

driver.find_element(By.CSS_SELECTOR,"img[alt='Cart']").click()  #15
driver.find_element(By.XPATH,"//button[text()='PROCEED TO CHECKOUT']").click()

#Sum validation
prices = driver.find_elements(By.CSS_SELECTOR,"tr td:nth-child(5) p")
total = 0
for price in prices:
    total = total + int(price.text)

print(total)
totalAmount = int(driver.find_element(By.CSS_SELECTOR, ".totAmt").text)

assert total == totalAmount
driver.find_element(By.CSS_SELECTOR,".promoCode").send_keys("rahulshettyacademy")
driver.find_element(By.CSS_SELECTOR,".promoBtn").click()
wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR,".promoInfo")))
print(driver.find_element(By.CLASS_NAME,"promoInfo").text)

driver.quit()
