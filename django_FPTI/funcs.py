import json

# def BoboSort(lista, criterio,qtd):
#     saida = []
#     k=0;
#     while((len(saida)<qtd) and k<len(lista)):
#         max = -100.0;
#         for i,item in enumerate(lista):
#             numero = []
#             for l in item[criterio]:
#                 if(l==','):
#                     numero.append('.');
#                 else:
#                     numero.append(l);
#             if(float(''.join(numero)) > max):
#                 max = float(item[criterio])
#                 selecionado = item;
#                 apagar = i;
#         lista.pop(apagar)
#         saida.append(selecionado);
#         k=k+1;
#     return saida




# def OrdenaScore(arquivo):
#     file = open(arquivo);
#     movies = json.load(file);
#     with open('Top20Score.json', 'w', encoding='utf-8') as f:
#         json.dump(BoboSort(movies, "imdbScore", 20), f, ensure_ascii=False, indent=4)
# OrdenaScore("successData.json")
# print(json.load(open('Top20Score.json')))
def normatizar(arquivo):
    file = open(arquivo, encoding="utf-8");
    movies = json.load(file);
    file.close
    for movie in movies:
        if "popularity" not in movie:
            movie["popularity"] = "0"
        if "popularityDelta" not in movie:
            movie["popularityDelta"] = "0"
        if 'UX190_' in movie["poster"]:
                    movie["poster"] = movie["poster"].replace('UX190_',"UX1900_")
        if 'UY281_' in movie["poster"]:
                    movie["poster"] = movie["poster"].replace('UY281_',"UY2810_")
        if ',190,281_.jpg' in movie["poster"]:
                    movie["poster"] = movie["poster"].replace(',190,281_.jpg',",1900,2810_.jpg")

    file = open(arquivo, "w")
    json.dump(movies, file, ensure_ascii=False, indent=4)
    file.close()