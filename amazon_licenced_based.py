import os
import requests
import pytesseract
import xlwings as xw
from time import sleep
from selenium import webdriver
from getmac import get_mac_address as gma
from selenium.webdriver.common import alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

URL = "http://amazon.quantrecenergy.in/api/mac.php"
system_mac = gma().strip()

system_mac = system_mac.replace("-", ":")
system_mac = system_mac.lower()

PARAMS = {'mac':system_mac}
r = requests.post(URL, PARAMS)
auth = r.text

if auth == "true":
    ws = xw.Book(r'details.xlsx').sheets("data")
    rows = ws.range("A2").expand().options(numbers=int).value

    driver = webdriver.Chrome(ChromeDriverManager().install()) 
    driver.maximize_window()


    # =====================================  function for login  ===================================
    def login():   
        email = driver.find_element_by_xpath("//label[contains(text(),'Email or mobile phone number')]//following::input").send_keys(row[0])
        button = driver.find_element_by_xpath("//label[contains(text(),'Email or mobile phone number')]//following::span").click()


    # ======================================  function for captcha read  =======================================
    def captha(): 
        driver.find_element_by_xpath("//label[contains(text(),'Password')]//following::input").send_keys(row[1])
        capta= driver.find_element_by_id('auth-captcha-image').screenshot('captcha.png')
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
        a = pytesseract.image_to_string(r'captcha.png')
        sleep(1)
        a = a.replace(" ", "")
        sleep(1)
        driver.find_element_by_xpath('//label[contains(text(),"Type characters")]//following::input').send_keys(a.lstrip())
        sleep(1)
        driver.find_element_by_id('signInSubmit').click()



    # ================================  function for add_password_error using Javascript  ===========================
    # def add_password_error():
    #     execu = '''
    #     var span = document.createElement("SPAN");   
    #     span.type = 'text/javascript';
    #     span.innerHTML = "Message and Data rates may apply.";                   
    #     document.body.appendChild(span);
    #     '''
    #     driver.execute_script(execu)
    #     sleep(2)


    # ====================================  function for password error  ===================================
    def passError():
        try:
            password = driver.find_element_by_xpath("//label[contains(text(),'Password')]//following::input").send_keys(row[1])
            signin = driver.find_element_by_xpath("//label[contains(text(),'Password')]//following::span").click()
        except:
            pass


    # ======================  function for all login, password error capthca, email error  =============================
    def authentication():
        try:
            sleep(1)
            i = 0
            try:
                capthatest = driver.find_element_by_xpath("//label[contains(text(),'Email or mobile phone number')] | //label[contains(text(),'Type characters')] | //span[contains(text(),'Message and Data rates may apply.')]").text
            except:
                pass
            
            # add_password_error() # =================== add_password_error function calling ====================
            try:
                while((capthatest=="Enter the characters you see") or (capthatest=="Email or mobile phone number") or (capthatest=="Message and Data rates may apply.") and (i<16)):

                    # add_password_error() # ================ add_password_error function calling ====================

                    capthatest = driver.find_element_by_xpath("//label[contains(text(),'Email or mobile phone number')] | //label[contains(text(),'Type characters')] | //span[contains(text(),'Message and Data rates may apply.')]").text

                    if capthatest == "Message and Data rates may apply.":
                        passError()
                    if capthatest == "Type characters":
                        captha()
                    if capthatest == "Email or mobile phone number":
                        login()
                    else:
                        pass
                    i+=1
                    sleep(1)
            except:
                pass    
        except:
            del capthatest


    # ==========================================  function for otp sending  ======================================
    def otp():   
        try:
            send_otp = driver.find_element_by_xpath('//*[@id="continue"]').click()
            sleep(30)
        except:
            pass


    # ==========================================  function for Login Approve  ======================================
    def login_approve():
        try:
            approve = driver.find_element_by_xpath('//span[text()="For your security, approve the notification sent to:"]')
            sleep(60)
        except:
            pass       


    # -------------------------------------  ##########################  ------------------------------------
    # =====================================  Start Automation From Here  ====================================
    # -------------------------------------  ##########################  ------------------------------------

    num = 2
    for row in rows:
        col = ws.range("I"+str(num)).value
        if (col == "Fail") or (col==None) or (col=="Server not response"):
            try:
                driver.get ("https://www.amazon.in/hfc/bill/electricity?ref_=apay_deskhome_Electricity")

                state_dropdown = driver.find_element_by_xpath('//span[text()="Select State"]').click()
                state = driver.find_element_by_xpath('//a[text()="Rajasthan"]').click()

                board = row[3].strip()
                board_dropdown = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, '//span[text()="Select Electricity Board to proceed"]'))
                )
                board_dropdown.click()
                driver.find_element_by_link_text(board).click()

                k_number = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, '//label[contains(text(), "K Number")]//following::input'))
                )

                # driver.get_cookies()
                # driver.delete_all_cookies()

                k_number.send_keys(row[4])
                fetch_bill = driver.find_element_by_xpath('//span[text()="Fetch Bill"]').click()
                
                sleep(2)
                bypass_id = driver.execute_script('document.querySelector("#paymentBtnId-announce").setAttribute("type", "submit")')

                try:
                    popup = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="a-popover-1"]/div'))
                        )
                    popup_text = popup.text 
                    # popup_text = popup_text.replace("\n", "")
                    sleep(1)
                    ws.range("H"+str(num)).value = "NA"
                    ws.range("I"+str(num)).value = popup_text
                    sleep(1)

                except:
                    element = WebDriverWait(driver, 50).until(
                        EC.presence_of_element_located((By.XPATH, '//span[contains(text(),"Continue to Pay")]'))
                    )

                sleep(1)
                res_amount = element.text
                res_amount = res_amount[17:]
                ws.range("G"+str(num)).value = res_amount

                sleep(1)
                amount = ws.range("F"+str(num)).value
                response_amount = ws.range("G"+str(num)).value     
                
                if amount == response_amount:
                    sleep(2)
                    element = WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Continue to Pay")]'))
                    )
                    element.click()
                else:
                    ws.range("H"+str(num)).value = "NA"
                    ws.range("I"+str(num)).value = "Amount miss Match"


                authentication() # ========================= login & captcha function calling ==========================
                login_approve()  # =====================  Login Approve screen Hold function calling ===================
                

                pay = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//input[@name="ppw-widgetEvent:SetPaymentPlanSelectContinueEvent"]')) )
                pay.click()
                
                sleep(15)
                otp()  # =====================  Otp screen function Calling function calling  ========================
                
                sleep(40)
                try:
                    success = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="deep-dtyp-success-alert"]/div/h4'))
                    )

                    pending = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="deep-dtyp-pending-widget"]/div/div/h4'))
                    )

                    fail = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="deep-dtyp-failed-widget"]/div/div/h4'))
                    )

                    if success.is_displayed():
                        status = success.text

                    elif pending.is_displayed():
                        status = pending.text

                    elif fail.is_displayed():
                        status = fail.text
                    else:
                        pass
                except:
                    pass

                try:
                    BBPS_Reference_Number = driver.find_element_by_xpath('//*[contains(text(), "BBPS Reference Number")]').text
                    bbps_num = BBPS_Reference_Number[23:]
                except:
                    pass

                sleep(1)
                try:
                    order = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Order #")]'))
                    )
                    order_id = order.text
                    order_ids = order_id[8:]
                except:
                    pass

                if "successful" in status:
                    ws.range("H"+str(num)).value = bbps_num
                    ws.range("I"+str(num)).value = "Success"

                elif "pending" in status:
                    ws.range("H"+str(num)).value = "NA"
                    ws.range("I"+str(num)).value = "Pending"
                    ws.range("J"+str(num)).value = order_ids

                else:
                    ws.range("H"+str(num)).value = "NA"
                    ws.range("I"+str(num)).value = "Fail"
            
            except:
                stat = ws.range("I"+str(num)).value
                if stat =="Fail" or stat == "Server not response" or stat==None:
                    ws.range("H"+str(num)).value = "NA"
                    ws.range("I"+str(num)).value = "Server not response"


        # =============================== For Remove Captcha Image ===================================
        try:
            os.remove('captcha.png')        
        except:
            pass


        num += 1
    driver.close()

else:
    print('''\n---------------------  #########################  ----------------------
    ==================== You have not Proper valid key  =========================
    ---------------------  #########################  ----------------------''')

input("\n\n\n========================= Press Enter  to exit ============================")