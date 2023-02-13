import pandas as pd

#dev purposes
#file = r"C:\Users\benai\Desktop\dev\Stock_verif-main\GLOVO.xlsx"
liste = ["bestsellers", "books in english","idées cadeaux","mangas", "livres en arabe", "livres pour enfants","romans made in morocco", "essais made in morocco", "beaux livres", "nouveautés", "développement personnel", "jeunesse"]

#préciser le type de dataframe dtype={'':str} en string pour avoir les bons isbn

def isbn_file_read(file):
    df = pd.read_excel(file, None, dtype={'ISBN':str})
    df = [df[elem]['ISBN'].dropna() for elem in liste]
    resultat = []
    for i in range(len(df)):
        resultat.append(df[i].tolist())
    
    resultat = [j for sub in resultat for j in sub] #flatten list (2D --> 1D)
    resultat = tuple(resultat)
    return resultat







