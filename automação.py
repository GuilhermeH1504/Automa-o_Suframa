from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotVisibleException, TimeoutException
import time
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

driver = webdriver.Chrome()

def automacao():
    driver.get("https://simnac.suframa.gov.br/#/notificacoes")
    driver.maximize_window()
    wait = WebDriverWait(driver, 20)

    # Login - CNPJ
    try:
        campo_cnpj = wait.until(
            EC.presence_of_element_located((By.NAME, "usuario"))
        )
        campo_cnpj.send_keys("17359233000188") 
    except ElementNotVisibleException:
        print("Elemento não visivel")
    except Exception as e:
        print(f"Erro ao preencher CNPJ, {e}")
    finally:
        time.sleep(0.5)

    # Login - Senha
    try:
        campo_senha = wait.until(
            EC.presence_of_element_located((By.NAME, "senha"))
        )
        campo_senha.send_keys('Tambasa1788')
    except Exception as e:
        print(f"Erro ao preencher senha, {e}")
    except ElementNotVisibleException:
        print("Elemento não visivel")
    finally:
        time.sleep(0.1)

    # Login - Click Button
    try:
        button_open = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        button_open.click()
        print("Login realizado com sucesso")
    except TimeoutException:
        print("Algum elemento não carregou dentro do tempo esperado")
    finally:
        time.sleep(0.5)

    # Navigate to Remetente (Navegando para o botão Remetente)
    try:
        acess_remetent = wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Remetente')]"))
        )
        acess_remetent.click()
    except Exception as e:
        print(f"Erro ao clicar no botão Remetente, {e}")
    except ElementNotVisibleException:
        print("Elemento não visivel")
    finally:
        time.sleep(0.5)

    # Navigate to Consultar Situação Cadastral (Navegando para o botão Consultar Situação Cadastral)
    try:
        consulta_situacao = wait.until(
            EC.presence_of_element_located((By.LINK_TEXT, "Consultar Situação Cadastral Destinatário"))
        )
        consulta_situacao.click()
    except TimeoutException:
        print("Botão de Consultar Situação não carregou como esperado")
    finally:
        time.sleep(0.5)

    # Process Excel Data (Processando dados da planilha excel)
    try:
        # Check if file exists would be good, but we'll trust the user's setup for now as per their code
        df = pd.read_excel("Suframa.xlsx")
        
        for index, row in df.iterrows():
            cnpj = row['CNPJ']
            print(f"Consultando CNPJ: {cnpj}")
            
            try:
                # Enter CNPJ (Inserindo o CNPJ)
                consult_cnpj = wait.until(
                    EC.presence_of_element_located((By.NAME, "cnpjDestinatario"))
                )
                #consult_cnpj.clear() 
                consult_cnpj.send_keys(cnpj)
                time.sleep(0.5)


                # Click Consult (Clicando no botão consultar)
                button_consult = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
                )
                button_consult.click()
                time.sleep(2) # Wait for results(Esperando resultados)

                # Check for "CNPJ não encontrado" modal
                try:
                    error_msg = driver.find_elements(By.XPATH, "//p[contains(text(), 'CNPJ não foi encontrado')]")
                    if error_msg:
                        print(f"CNPJ {cnpj} não encontrado.")
                        df.loc[index, 'Status Suframa'] = "CNPJ não foi encontrado."
                        
                        # Close the modal
                        close_btn = driver.find_element(By.XPATH, "//button[contains(., 'Fechar')]")
                        close_btn.click()
                        time.sleep(1)
                        continue # Skip to next iteration (Pulando para a próxima iteração)
                except Exception as e:
                    print(f"Erro ao verificar modal de erro: {e}")

                # Get Status (Conferindo status)
                situacao_cadastral = wait.until(
                    EC.presence_of_element_located((By.ID, "situacaoCadastralAtual"))
                )

                # Voltando uma tela
                returnando_tela = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Voltar')]")) # Sempre que estiver elementos igual usar o XPATH para buscar pelo texto.
                )
                returnando_tela.click()
                time.sleep(0.1)


                status = situacao_cadastral.get_attribute("value") # Pegando um texto que esta dentro de um elemento
                print(f"Status: {status}")
                df.loc[index, 'Status Suframa'] = status

                df.loc[index, 'DATA'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S') # Adicionando datas na coluna de DATA
                
            except TimeoutException:
                print(f"Timeout ao consultar CNPJ {cnpj}")
            except Exception as e:
                print(f"Erro ao consultar CNPJ {cnpj}: {e}")
            
            finally:
                time.sleep(0.5)
            
    except Exception as e:
        print(f"Erro ao ler ou processar arquivo Excel: {e}")
    finally:
        # Save results (Salvando resultados)
        try:
            if 'df' in locals():
                df.to_excel("Suframa.xlsx", index=False)
                print("Dados salvos com sucesso")
        except Exception as e:
            print(f"Erro ao salvar dados na planilha, {e}")

automacao()
