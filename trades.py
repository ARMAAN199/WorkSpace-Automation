from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ARMAAN
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import random
from config import *
from multiprocessing import Pool
from selenium.webdriver.common.keys import Keys as KEYS
import sys

import os
def automate_trades(i, driver):
    try:
        element =  WebDriverWait(driver, 40).until(
            ARMAAN.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]/span')))
        element.click()
        print("Going to Strategies Page")
    except:
        automate_trades(i,driver)
        return

    tradegroup_count = find_tradegroup_count(i, driver)
    if tradegroup_count == 0:
        return
    print("TradeGroups Found : ", tradegroup_count)
    # Choosing a TradeGroup
    group_name, chosenGroup = choose_and_name(i, driver, 1, tradegroup_count, tradegroupPath)
    print(group_name)
    # Choosing Trade in TradeGroup
    trade_count = find_trade_count(i, driver, chosenGroup)
    print("Trades Found : ", trade_count)
    tradeNamePath[0] = tradeNamePath[0] + str(chosenGroup) + tradeNamePath[2]
    trade_name , chosenTrade = choose_and_name(i, driver, 1, trade_count, tradeNamePath, 0)
    print(trade_name)
    buyOrderWindowPath[0] = buyOrderWindowPath[0] + str(chosenGroup) + buyOrderWindowPath[2] + str(chosenTrade)
    choose_and_name(i, driver, 2, 1, buyOrderWindowPath)
    delta_val = readTradeWindow(i, driver)
    randomize_inputs(i, driver, delta_val)


def choose_and_name(i, driver, min , max, path, click = 1):
    if min > max:
        chosen = ""
    else:
        chosen = random.randint(min, max)
    time.sleep(0.4)
    # print(path[0] + str(chosen) + path[1])
    try:
        actions = ActionChains(driver)
        ele = WebDriverWait(driver, 5).until(
                ARMAAN.presence_of_element_located((By.XPATH, path[0] + str(chosen) + path[1])))
        actions.move_to_element(ele).perform()
        name = ele.get_attribute("innerHTML")
        if click == 1:
            ele.click()
            return [name, chosen]
        else:
            return ["nil", chosen]
    except:
        print("error")
        return

def find_tradegroup_count(i, driver):
    try:
        tradegrouplist = WebDriverWait(driver, 5).until(
                ARMAAN.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[3]/div[2]')))
        trades_grups = tradegrouplist.find_elements(by=By.XPATH, value="*")
        return len(trades_grups)
    except:
        print("No Trade Groups Found")


def find_trade_count(i, driver, chosen):
    try:
        tradelist = WebDriverWait(driver, 5).until(
                ARMAAN.presence_of_element_located((By.XPATH, tradesPath[0] + str(chosen) + tradesPath[1])))
        trades = tradelist.find_elements(by=By.XPATH, value="*")
        return len(trades)
    except:
        print("No Trades Found")


def readTradeWindow(i, driver):
    try:
        ele = WebDriverWait(driver, 15).until(ARMAAN.presence_of_element_located((By.XPATH, orderwindow_title[0])))
        window_title = ele.get_attribute("innerHTML")
        print("Opened Window : ", window_title)
    except:
        print("unable to open trade window")
        return
    dp = read_delta(i, driver)
    print("delta : ", dp)
    return dp
    # except:
    #     print("unable to read delta, cancelling thread")

def read_delta(i, driver):
    ele = WebDriverWait(driver, 15).until(ARMAAN.presence_of_element_located((By.XPATH, delta[0])))
    delta_price = ele.get_attribute("innerHTML")
    return delta_price


def randomize_inputs(i, driver, delta_val):
    badla_input = WebDriverWait(driver, 15).until(ARMAAN.presence_of_element_located((By.XPATH, inputs[0])))
    lots_input = WebDriverWait(driver, 15).until(ARMAAN.presence_of_element_located((By.XPATH, inputs[1])))
    lots_pc_input = WebDriverWait(driver, 15).until(ARMAAN.presence_of_element_located((By.XPATH, inputs[2])))
    order_button =
    badla_input.send_keys(Keys.CONTROL, "a")
    variability = random.uniform(-10, 20)
    delta_val = float(delta_val)
    badla_val = delta_val + ((delta_val * variability)/100)
    print("Taking Badla with a variability of plus-minus 20% of delta, calculated badla val : ", badla_val)
    badla_input.send_keys(badla_val)
    lots_input.send_keys(Keys.CONTROL, "a")
    lots_val = random.randint(-1000, 3000)
    print("lots val : ", lots_val)
    lots_input.send_keys(lots_val)
    lots_pc_input.send_keys(Keys.CONTROL, "a")
    lots_pc_val = random.randint(-1000, 3000)
    print("lots pc val : ", lots_pc_val)
    lots_pc_input.send_keys(lots_pc_val)
    time.sleep(10)



def opened_trade_name(i,driver, chosen):
    tradename = WebDriverWait(driver, 5).until(
        ARMAAN.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[3]/div["+str(chosen)+"]/div[1]/div[2]/span"))).get_attribute("innerHTML")
    return tradename


# def work_trade_window(i, driver):
#
#
#
# /html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[3]/div[2]/div[2]/div[3]/div/div
# /html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[3]/div[3]/div[2]/div[3]/div/div


'''
/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[3]/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/div/i
/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[3]/div[2]/div[1]/div[2]/div[1]/div[3]/div[1]/div/i

/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[3]/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]/div/i
/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[3]/div[2]/div[2]/div[2]/div[2]/div[3]/div[1]/div/i

/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[3]/div[2]/div[1]/div[2]/div[3]/div[3]/div[1]/div/i

/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[3]/div[2]/div[4]/div[2]/div[1]/div[2]/div[1]/div/i
/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[3]/div[2]/div[4]/div[2]/div[1]/div[3]/div[1]/div/i



/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[3]/div[2]/div[]/div[1]/span"

/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[3]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/span
/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[3]/div[2]/div[1]/div[2]/div[2]

/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[3]/div[2]/div[3]/div[2]/div

/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[3]/div[2]/div[4]/div[2]/div[1]
/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[3]/div[2]/div[4]/div[2]/div[2]

/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[3]/div[2]/div[4]/div[2]

/html/body/div[2]/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/div[1]/div/div/input
/html/body/div[2]/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/div[1]/div/div/input

/html/body/div[2]/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/div[2]/div/div/input
/html/body/div[2]/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div[1]/div/div/input

'''