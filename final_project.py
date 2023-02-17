#All import
import json
import csv
import urllib
from bs4 import BeautifulSoup as bs
import requests
import re

def connexion(i, brand):
    """_summary_

    Args:
        url (_string_): _url with incrementation of the website page_
        brand (_string_): _store one specific brand_
        html_doc (_script_): _store the current information of the page_
        data (_json_): _store the json_

    Returns:
        _data_: _Json data_
    """
    
    if(brand == "n"):
        url = "https://www.lacentrale.fr/listing?makesModelsCommercialNames=&options=&page=" + str(i)
        html_doc = requests.get(url).text
        data = re.search(r"window.__PRELOADED_STATE_LISTING__ =(.*?);", html_doc) # Ou aussi "({.?})"        
        data = json.loads(data.group(1))
        return data
    else:
        url = "https://www.lacentrale.fr/listing?makesModelsCommercialNames="+ str(brand) +"&options=&page=" + str(i)
        html_doc = requests.get(url).text
        data = re.search(r"window.__PRELOADED_STATE_LISTING__ =(.*?);", html_doc) # Ou aussi "({.?})"        
        data = json.loads(data.group(1))
        return data
    
def brand_choice():
    """_summary_
        Verification of the type of the user brand choice
    Args:
        brand (_string_): _verification if the user want one specific brand_
        val (_string_): _store the brand in lower case_
    Returns:
        _string_: _return the brand or n_
    """
    
    brand = input("Choissez une marque : ")
    brand = brand.lower()
    try:
        val = str(brand)
        return val
    except ValueError:
        print("Ce n'est pas un mot !")
        brand_choice()
    

def search_json(data, nb, choice):
    """_summary_
    Args:
        data (_string_): _store the json_
        nb (_int_): _current card_
        list (_list_): _create a list with all the information of the current card_
        choice (_int_) _two type -1 or 1 for condition_

    Returns:
        _list_: _return all the information of the current card_
    """
    
    list = []
    if(choice != -1):
        try:
            list.append(data['search']['hits'][nb]['item']['vehicle']['make'])
        except IndexError:
            print("Veuillez choissir une marque existante !")
            exit()
    #KeyError
    try:
        list.append(data['search']['hits'][nb]['item']['vehicle']['detailedModel'])
    except KeyError:
        list.append(data['search']['hits'][nb]['item']['vehicle']['model'])
    list.append(data['search']['hits'][nb]['item']['vehicle']['version'])
    list.append(int(data['search']['hits'][nb]['item']['vehicle']['year']))
    list.append(int(data['search']['hits'][nb]['item']['vehicle']['mileage']))
    list.append(data['search']['hits'][nb]['item']['vehicle']['energy'])
    list.append(int(data['search']['hits'][nb]['item']['price']))
    return list
    
def csv_writer(list):
    """_summary_
    _Write the information of the current card in the csv_
    Args:
        list (_list_): _all the information of the current card_
        writer (_csv_): _store the current csv file_
    """
    
    with open('results.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(list)
        
def page_choice():
    """_summary_
    _Verification of the type of the user input_
    Args:
        nbr(_?_): _The number of the page the user want to scrapp_
        val(_int_): _store the user choice (int)_
    
    Returns:
        _val_: _The number of the page the user want to scrapp_
    """
    
    nbr = input ("Combien de page(s) voulez-vous scrap ? ")
    try:
        val = int(nbr)
        return val
    except ValueError:
        print("Ce n'est pas un entier!")
        page_choice()
        
        
def write_brand(list):
    """_summary_
    write the current brand in csv file
    Args:
        list (_list_): _store all the brand_
        writer (_csv_): _store the csv file_
    """
    with open('results_brand.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(list)
        
def find_brand(data):
    """_summary_
    find all the brand of the website and model
    Args:
        size_all (_int_): _store the length of the list_
        data (_json_): _store the information of the current page_
        list (_list_): _store the information of the brand_
    """
    size_all = len(data['search']['aggs']['vehicle.make'])
    for i in range(0, size_all):
        list = []
        size_brand = len(data['search']['aggs']['vehicle.make'][i]['agg'])
        list.append(data['search']['aggs']['vehicle.make'][i]['key'])
        for j in range(0, size_brand):
            list.append(data['search']['aggs']['vehicle.make'][i]['agg'][j]['key'])
        write_brand(list)
        
def find_brand_with(data, brand):
    """_summary_
    find all the model of one specific brand
    Args:
        data (_json_): _store the information of the current page_
        brand (_string_): _store one specific brand_
        list (_list_): _store all the model of the brand without the brand_
        list_wname (_list_): store all the model of the brand with the brand_
        name (_string_): _store the name of the current brand_ 

    Returns:
        _list_: _store all the information of the model without the name_
    """
    brand = brand.upper()
    try:
        data['search']['hits'][0]['item']['vehicle']['make']
    except IndexError:
        print("Veuillez choissir une marque existante !")
        exit()
    size_all = len(data['search']['aggs']['vehicle.make'])
    for i in range(0, size_all):
        list_wname = []
        list = []
        size_brand = len(data['search']['aggs']['vehicle.make'][i]['agg'])
        name = data['search']['aggs']['vehicle.make'][i]['key']
        list_wname.append(name)
        if(name == brand):
            for j in range(0, size_brand):
                list_wname.append(data['search']['aggs']['vehicle.make'][i]['agg'][j]['key'])
                list.append(data['search']['aggs']['vehicle.make'][i]['agg'][j]['key'])
            write_brand(list_wname)   
            return list

def search_brand_and_modele(data, brand):
    """_summary_

    Args:
        data (_json_): _store the information of the current page_
        brand (_string_): _store the current brand_

    Returns:
        _list_: _store all the brand without or with a brand_
    """
    if(brand != "n"):
        return find_brand_with(data, brand)
    else:
        return find_brand(data)
        
def scrapp_website(data, brand, nb_pages):
    """_summary_

    Args:
        data (_json_): _store all the information of the current page_
        brand (_string_): _store the current brand_
        nb_pages (_int_): _store the number of page the user want to scrapp_
        content (_int_): _store the total number of card_
    """
    i = 1
    nb_pages_officiel = (data['search']['total']//16)+1
    if(nb_pages > nb_pages_officiel):
        print("Il n'y à pas assez d'annonce ! Ou la marque est invalide")
        nb_pages = nb_pages_officiel
    while(i <= nb_pages):
        data = connexion(i, brand)
        content = data['search']['total']
        if(content > 16):
            content = 16
        for j in range(0,content):
            csv_writer(search_json(data, j, 1))
        i += 1

def lauch():
    """_summary_
    first fonction in action, selection of what the user want to do
    """
    user_choice = int(input("1: Scrapp cards; 2: Scrapp cards avec marque; 3: Récupérer toutes les marques; 4: Récupérer tout les modèles d'une marque : "))
    if user_choice == 1:
        nb_pages = page_choice()
        data = connexion(nb_pages, "n")
        scrapp_website(data, "n", nb_pages)
        
    elif user_choice == 2:
        nb_pages = page_choice()
        brand = brand_choice()
        data = connexion(nb_pages, brand_choice)
        scrapp_website(data, brand, nb_pages)
        
    elif user_choice == 3:
        data = connexion(1, brand_choice)
        search_brand_and_modele(data, "n")
    elif user_choice == 4:
        brand = brand_choice()
        data = connexion(1, brand)
        search_brand_and_modele(data, brand)
 
#------------------------------------------------------------------------------------------       
#SCRAPP 2 pages of all the model of one brand
    """_summary_
    Récupérer une marque
    Récupérer les modèles d’une marque

    Boucle modèle total
        Connexion p1
        Combien de page
        boucle total page max 3
            Récupérer les infos des cards
            Ajouter information card
        Ecrire csv
	

    """
#------------------------------------------------------------------------------------------
def connexion_2(i, brand, modele):
    """_summary_

    Args:
        url (_string_): _url with incrementation of the website page_
        brand (_string_): _verification if the user want one specific brand_
        data (_json_): _store the json_

    Returns:
        _data_: _Json data_
    """
    
    if(brand == "n"):
        url = "https://www.lacentrale.fr/listing?makesModelsCommercialNames=&options=&page=" + str(i)
        html_doc = requests.get(url).text
        data = re.search(r"window.__PRELOADED_STATE_LISTING__ =(.*?);", html_doc) # Ou aussi "({.?})"        
        data = json.loads(data.group(1))
        
        return data
    else:
        url = "https://www.lacentrale.fr/listing?makesModelsCommercialNames="+ str(brand) +"%3A" + str(modele) + "&options=&page=" + str(i)
        html_doc = requests.get(url).text
        data = re.search(r"window.__PRELOADED_STATE_LISTING__ =(.*?);", html_doc) # Ou aussi "({.?})"        
        data = json.loads(data.group(1))
        return data

def scrapp_website_2(data, brand, nb_pages, modele, content):
    i = 1
    while(i <= nb_pages):
        data = connexion_2(i, brand, modele)
        for j in range(0,content):
            csv_writer(search_json(data, j, -1))
        i += 1


    
def f1():
    
    brand = brand_choice()
    data = connexion(1, brand)
    modeles = search_brand_and_modele(data, brand)
    if(modeles == None):
        print("Marque inexistante !")
        exit()
    size_modeles = len(modeles)
    for i in range(0, size_modeles):
        data_2 = connexion_2(1, brand, modeles[i])
        content = data_2['search']['total']
        if(content > 16):
            content = 16
        nb_pages = (data_2['search']['total']//16)+1
        if(nb_pages == 1):
            scrapp_website_2(data_2, brand, 1, modeles[i], content)
        elif(nb_pages > 2):
            scrapp_website_2(data_2, brand, 2, modeles[i], content)
        

            
if __name__ == "__main__" :
    lauch()
    #f1()

    
#print(data['search']['hits'][0]['item']['vehicle']['make']) Iteration exemple