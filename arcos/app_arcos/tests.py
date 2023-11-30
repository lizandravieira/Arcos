from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import random
import string
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
browser = webdriver.Chrome(options=chrome_options)

username = ''.join(random.choices(string.ascii_lowercase, k=8))
password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

class TestSignupLogin(TestCase):
    def test_a_create_ong(self):
        browser.get('http://127.0.0.1:8000')
        browser.find_element(By.XPATH, "/html/body/main/div/a").click()
        time.sleep(3)

        assert browser.current_url == "http://127.0.0.1:8000/login/"
    
    def test_b_register_ong(self):
        browser.get("http://127.0.0.1:8000/login/")
        browser.find_element(By.XPATH,"/html/body/main/div/div/form/div[3]/a").click()
        time.sleep(3)   

        assert browser.current_url == "http://127.0.0.1:8000/register/"

        browser.find_element(By.XPATH,"/html/body/main/div/div/form/div[1]/input").send_keys(username +"ong")
        time.sleep(3)
        browser.find_element(By.XPATH,"/html/body/main/div/div/form/div[2]/input").send_keys(username)
        time.sleep(3)   
        browser.find_element(By.XPATH,"/html/body/main/div/div/form/div[3]/input").send_keys(username + "@gmail.com")
        time.sleep(3)
        browser.find_element(By.XPATH,"/html/body/main/div/div/form/div[4]/input ").send_keys(password)
        time.sleep(3)
        browser.find_element(By.ID,"button").click()
      
      
        assert browser.current_url == "http://127.0.0.1:8000/org/panel"

    def test_c_create_contact(self):
        browser.find_element(By.XPATH,"/html/body/header/nav/div/div/ul[1]/li[2]/a").click()
        time.sleep(3)
        browser.find_element(By.XPATH,"/html/body/main/div/div/form/div[1]/input").send_keys(username + "@gmail.com")
        time.sleep(3)
        browser.find_element(By.XPATH, "/html/body/main/div/div/form/div[2]/input").send_keys("123456789")
        time.sleep(3)
        browser.find_element(By.XPATH, "/html/body/main/div/div/form/div[3]/input").send_keys("@testes")
        time.sleep(3)
        browser.find_element(By.XPATH, "/html/body/main/div/div/form/div[4]/input").send_keys("@testes")
        time.sleep(3)
        browser.find_element(By.XPATH, "/html/body/main/div/div/form/button").click()
        time.sleep(3)

        assert browser.current_url == "http://127.0.0.1:8000/org/panel/contact"

    def test_d_create_action(self):
        browser.find_element(By.XPATH, "/html/body/header/nav/div/div/ul[1]/li[3]/a").click()
        time.sleep(3)
        browser.find_element(By.XPATH, "/html/body/main/div/a").click()
        time.sleep(3)
        browser.find_element(By.XPATH, "/html/body/main/div/div/form/div[1]/input").send_keys("ação teste")
        time.sleep(3)
        browser.find_element(By.XPATH, "/html/body/main/div/div/form/div[2]/input").send_keys("02")
        time.sleep(3)
        browser.find_element(By.XPATH, "/html/body/main/div/div/form/div[3]/input").send_keys("09")
        time.sleep(3)
        browser.find_element(By.XPATH, "/html/body/main/div/div/form/div[4]/input").send_keys("2021")
        time.sleep(3)
        file_input = browser.find_element(By.XPATH, "/html/body/main/div/div/form/div[5]/input")
        time.sleep(3)
        file_input.send_keys(r"C:\Users\Pedro Lira\Downloads\imagem acao teste.jpeg")
        time.sleep(3)
        file_input = browser.find_element(By.XPATH, "/html/body/main/div/div/form/div[6]/input")
        time.sleep(3)
        file_input.send_keys(r"C:\Users\Pedro Lira\Downloads\imagem azul anexo.jpeg")
        time.sleep(3)
        browser.find_element(By.XPATH, "/html/body/main/div/div/form/div[7]/textarea").send_keys("teste")
        time.sleep(3)
        browser.find_element(By.XPATH, "/html/body/main/div/div/form/button").click()
        time.sleep(3)
        browser.find_element(By.XPATH, "/html/body/main/div/div/form/div[1]/input").send_keys("teste1")
        time.sleep(3)
        browser.find_element(By.XPATH, "/html/body/main/div/div/form/div[2]/input").send_keys("12")
        time.sleep(3)
        browser.find_element(By.XPATH, "/html/body/main/div/div/form/div[3]/input").send_keys("19")
        time.sleep(3)
        browser.find_element(By.XPATH, "/html/body/main/div/div/form/div[4]/input").send_keys("2021")
        time.sleep(3)
        file_input = browser.find_element(By.XPATH, "/html/body/main/div/div/form/div[5]/input")
        time.sleep(3)
        file_input.send_keys(r"C:\Users\Pedro Lira\Downloads\resumo-de-fundo-vermelho-circular_8466-2.avif")
        time.sleep(3)
        file_input = browser.find_element(By.XPATH, "/html/body/main/div/div/form/div[6]/input")
        time.sleep(3)
        file_input.send_keys(r"C:\Users\Pedro Lira\Downloads\fundo-gradiente-geometrico-amarelo-abstrato_1409-1846.avif")
        time.sleep(3)
        browser.find_element(By.XPATH, "/html/body/main/div/div/form/div[7]/textarea").send_keys("teste")
        time.sleep(3)
        browser.find_element(By.ID, "button").click()
        time.sleep(3)
        browser.find_element(By.XPATH, "/html/body/header/nav/div/div/ul[1]/li[3]/a").click()
        time.sleep(3)
        browser.find_element(By.XPATH,"/html/body/main/div/div/div[1]/div[2]/a").click()

        assert browser.current_url == "http://127.0.0.1:8000/org/panel/actions"
        
    
    def test_f_settings(self):
        time.sleep(3)
        browser.find_element(By.XPATH, "/html/body/header/nav/div/div/ul[1]/li[4]/a").click()
        time.sleep(3)
        select_element = browser.find_element(By.XPATH,"/html/body/main/div/div/form/div[1]/select")
        select = Select(select_element)
        select.select_by_index(1)
        time.sleep(3)
        color_input = browser.find_element(By.XPATH, "/html/body/main/div/div/form/div[2]/input")
        color_input.send_keys("#FF0000")
        time.sleep(3)
        file_input = browser.find_element(By.XPATH, "/html/body/main/div/div/form/div[3]/input")
        time.sleep(3)
        file_input.send_keys(r"C:\Users\Pedro Lira\Downloads\imagem acao teste.jpeg")
        time.sleep(3)
        select_element = browser.find_element(By.XPATH,"/html/body/main/div/div/form/div[4]/select")
        select = Select(select_element)
        select.select_by_index(0)
        time.sleep(3)
        browser.find_element(By.XPATH, "/html/body/main/div/div/form/button").click()
        time.sleep(3)
        
        #assert browser.current_url == "http://127.0.0.1:8000/org/panel/settings"

        browser.find_element(By.XPATH,"/html/body/header/nav/div/div/ul[1]/li[1]/a").click()
        time.sleep(3)
        browser.find_element(By.XPATH,"/html/body/main/div/a").click()
        time.sleep(3)
        browser.get('http://127.0.0.1:8000/view/site/username')
        time.sleep(3)
        assert browser.current_url == "http://127.0.0.1:8000/view/site/username"

        browser.get("http://127.0.0.1:8000/org/panel")
        time.sleep(3)
        browser.find_element(By.XPATH,"/html/body/header/nav/div/div/ul[1]/li[4]/a").click()
        time.sleep(3)
        select_element = browser.find_element(By.XPATH,"/html/body/main/div/div/form/div[1]/select")
        select = Select(select_element)
        select.select_by_index(0)   
        time.sleep(3)
        browser.find_element(By.XPATH,"/html/body/main/div/div/form/button").click()
        time.sleep(3)
        
        assert browser.current_url == "http://127.0.0.1:8000/org/panel/settings"

    def test_g_create_donation(self):
        time.sleep(3)
        browser.find_element(By.XPATH,"/html/body/header/nav/div/div/ul[1]/li[5]/a").click()
        time.sleep(3)
        browser.find_element(By.XPATH,"/html/body/main/div/div/div/form/div[1]/textarea").send_keys("descricao teste doacao")
        time.sleep(3)   
        browser.find_element(By.XPATH,"/html/body/main/div/div/div/form/div[2]/input").send_keys("chaveteste")
        time.sleep(3)
        browser.find_element(By.XPATH,"/html/body/main/div/div/div/form/div[3]/input").send_keys("projeto teste")
        time.sleep(3)
        browser.find_element(By.XPATH,"/html/body/main/div/div/div/form/button").click()
        time.sleep(3)
        browser.find_element(By.XPATH,"").click()

        assert browser.current_url == "http://127.0.0.1:8000/org/panel/donations/list"
    
    def test_h_add_coment(self):
        time.sleep(3)
        browser.get("http://127.0.0.1:8000/view/site/"+ username)
        time.sleep(3)
        browser.find_element(By.XPATH,"/html/body/header/nav/div/div/ul/li[2]/a").click()
        time.sleep(3)
        browser.find_element(By.XPATH,"/html/body/main/div/a/div[2]").click()
        time.sleep(3)
        browser.find_element(By.XPATH,"/html/body/main/div[2]/form/div[1]/input").send_keys(username)
        time.sleep(3)
        browser.find_element(By.XPATH,"/html/body/main/div[2]/form/div[2]/textarea").send_keys("comentario")
        time.sleep(3)
        browser.find_element(By.XPATH,"/html/body/main/div[2]/form/button").click()


        assert browser.current_url == f"http://127.0.0.1:8000/view/site/{username}/actions/3"

    def test_i_viewing_contact_page(self):
        time.sleep(3)
        browser.find_element(By.XPATH,"/html/body/header/nav/div/div/ul/li[3]/a").click()
        time.sleep(3)
        assert browser.current_url == f"http://127.0.0.1:8000/view/site/{username}/contact"
    
    def test_j_make_donation(self):
        time.sleep(3)
        browser.find_element(By.XPATH,"//html/body/header/nav/div/div/ul/li[4]/a").click()
        time.sleep(3)
        browser.find_element(By.XPATH,"/html/body/main/div/form/div[1]/input").send_keys("pedro")
        time.sleep(3)
        browser.find_element(By.XPATH,"/html/body/main/div/form/div[2]/input").send_keys("123")
        time.sleep(3)
        browser.find_element(By.XPATH,"/html/body/main/div/form/div[3]/input").send_keys("100")
        time.sleep(5)
        browser.find_element(By.ID,"/html/body/main/div/form/button[1]").click()
        time.sleep(3)
        
        assert browser.current_url == f"http://127.0.0.1:8000/view/site/{username}/donate"

    def test_h_accpet_donation(self):
        time.sleep(3)
        browser.get("http://127.0.0.1:8000/org/panel")
        time.sleep(3)
        browser.find_element(By.XPATH,"/html/body/header/nav/div/div/ul[1]/li[5]/a").click()
        time.sleep(3)
        browser.find_element(By.XPATH,"/html/body/main/div/div/div/form/a").click()
        time.sleep(3)
        browser.find_element(By.XPATH,"/html/body/main/div/div/a").click()

        assert browser.current_url == "http://127.0.0.1:8000/org/panel/donations/list"

        browser.find_element(By.XPATH,"/html/body/header/nav/div/div/ul[1]/li[1]/a").click()
        time.sleep(3)
        browser.find_element(By.XPATH,"/html/body/main/div/a").click()
        time.sleep(3)
        browser.get("http://127.0.0.1:8000/view/site/"+ username)
        time.sleep(3)
        browser.find_element(By.XPATH,"/html/body/header/nav/div/div/ul/li[4]/a").click()
        time.sleep(3)
        browser.find_element(By.XPATH,"/html/body/main/div/form/div[3]/input").send_keys(username+"123")
        time.sleep(3)
        browser.find_element(By.XPATH,"/html/body/main/div/form/button[2]").click()
        time.sleep(5)

     











        