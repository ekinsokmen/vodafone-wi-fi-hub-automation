import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

import argparse

parser = argparse.ArgumentParser(description='Add/remove public port mapping to Vodafone Wifi Hub')
parser.add_argument('-p', '--admin_pass', type=str, help='Admin password of the router', required=True)
parser.add_argument('--url', type=str, help='Base URL of the router like http://192.168.0.1', required=True)
parser.add_argument('cmd', type=str, choices=['add', 'remove'], help='Add or remove a public port mapping')
parser.add_argument('service_name', type=str, help='Name of the service to expose')
parser.add_argument('ip', type=str, help='IP of the service to expose')
parser.add_argument('lan_port', type=str, help='Port of the service to expose')
parser.add_argument('wan_port', type=str, help='Public port of the service to expose')
args = parser.parse_args()

ip_parts=args.ip.split('.')

if len(ip_parts) != 4:
  raise Exception("IP[{0}] address not in correct format.".format(args.ip))

class PortManager():

  def setupChrome(self):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument('--headless')
    self.driver = webdriver.Chrome(options=chrome_options)
    self.driver.implicitly_wait(20)
    self.wait = WebDriverWait(self.driver, 20)
  
  def teardown(self):
    self.driver.quit()
  
  def __gotoAddPortPage(self):
    self.driver.set_window_size(1280, 1080)
    self.driver.get(args.url)

    self.__setInputValueById("login-txt-pwd", args.admin_pass)
    self.driver.find_element(By.ID, "login-btn-logIn").click()
    self.driver.find_element(By.CSS_SELECTOR, "#Internet > span").click()
    self.driver.find_element(By.ID, "port-mapping").click()
    self.wait.until(expected_conditions.element_to_be_clickable((By.ID, "portmap-btn-add")))

  def __moveAndclickElement(self, element):
    action = ActionChains(self.driver)
    action.move_to_element(element).click().perform()

  def __clickById(self, id):
    self.wait.until(expected_conditions.element_to_be_clickable((By.ID, id)))
    self.driver.execute_script("document.getElementById(arguments[0]).click()", id)

  def __setInputValueById(self, id, value):
    self.wait.until(expected_conditions.element_to_be_clickable((By.ID, id)))
    self.driver.execute_script("document.getElementById(arguments[0]).value=arguments[1]", id, value)

  def addport(self):
    self.__gotoAddPortPage()
    self.__clickById("portmap-btn-add")
    self.__setInputValueById("portmap-txt-addService", args.service_name)

    self.driver.find_element(By.CSS_SELECTOR, "#portmap_sel_addProtocol_chosen span").click()
    self.driver.find_element(By.CSS_SELECTOR, ".active-result:nth-child(1)").click()
    self.__setInputValueById("portmap-txt-addIP1", ip_parts[0])
    self.__setInputValueById("portmap-txt-addIP2", ip_parts[1])
    self.__setInputValueById("portmap-txt-addIP3", ip_parts[2])
    self.__setInputValueById("portmap-txt-addIP4", ip_parts[3])
    self.__setInputValueById("portmap-txt-addWanPort", args.wan_port)
    self.__setInputValueById("portmap-txt-addLanPort", args.lan_port)
    self.__clickById("portmap-btn-addSave")
    portRule = self.driver.find_element(By.XPATH, "//tr[@class='portmap-rule']/td[contains(text(), '{0}')]".format(args.service_name))
    assert portRule
    self.__clickById("global-apply")
  
  def removePort(self):
    self.__gotoAddPortPage()
    portRule = self.driver.find_element(By.XPATH, "//tr[contains(@class,'portmap-rule')]/td[contains(text(),'{0}')]".format(args.service_name))
    assert portRule
    self.wait.until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, "button-delete")))
    deleteButton = portRule.parent.find_element(By.CLASS_NAME, "button-delete")
    assert deleteButton
    self.__moveAndclickElement(deleteButton)
    self.__clickById("global-apply")

addPortCommand = PortManager()
addPortCommand.setupChrome()
print("Browser ready.")

match args.cmd:
  case 'add':
    print("Adding port for service {0} on {1}->{2}:{3}".format(args.service_name, args.wan_port, args.ip, args.lan_port))
    addPortCommand.addport()
  case 'remove':
    print("Removing port for service {0}".format(args.service_name))
    addPortCommand.removePort()

time.sleep(15)

addPortCommand.teardown()

print("Done.")
