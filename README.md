# Universidade Estadual de Campinas
# Instituto da Computação

## Disciplina: MC855-2s2022

#### Professor e Assistente

| Nome                     | Email                   |
| ------------------------ | ------------------------|
| Professora Juliana Borin | jufborin@unicamp.br     |
| Assistente Paulo Kussler | paulo.kussler@gmail.com |


#### Equipe

| Nome               | RA               | Email                  | ID Git                |
| ------------------ | ---------------- | ---------------------- |---------------------- |
|Heigon Alafaire Soldera Pires|217638|h217638@dac.unicamp.br|heigon77|
|Piethro César de Andrade|223549|p223549@dac.unicamp.br|PiethroCesar|

### Descrição do projeto:
O projeto consiste em desenvolver uma plataforma que possui o objetivo de recomendar filmes ao usuários baseado em seus gostos.  
Esse repositório é destinado ao ambiente back-end do projeto.  

#### Prints das telas com descrição das funcionalidades. 
  
Por se tratar do back-end, não possui telas, porém possui os seguintes endpoints:  
  
#### Cadastro:  

Cria uma conta no banco de dados.

<details> 
  <summary>POST https://filmes-pra-ti.azurewebsites.net/auth/signup/ </summary>
   
```
body
{
"email": "teste@email.com",
"username": "user",
"password": "test1234"
}
```
```
response
{
  "message": "User Created Successfully",
  "data": {
    "email": "teste@email.com",
    "username": "user"
  }
}
```
</details>

As informações de senha armazenadas no banco são imediatamente encriptadas utilizando SHA256.

#### Login:  

Logar com o usuário criado e receber o token de autenticação.

<details> 
  <summary>POST https://filmes-pra-ti.azurewebsites.net/auth/login/ </summary>
   
```
body
{
  "email": "teste@email.com",
  "password": "test1234"
}
```
```
response
{
  "message": "Login Successfull",
  "username": "user",
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY4NDM4NjE4LCJpYXQiOjE2NjgzNjY2MTgsImp0aSI6IjQ2ZmI5YWMwOTY1YjQ1YWI5MDk0MzE3Nzg3ZTNhM2RjIiwidXNlcl9pZCI6M30._Ts9BddJ93qd5UUE3GbGnXwPnppkHbE5RtYZscKpjjU",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY2ODQ1MzAxOCwiaWF0IjoxNjY4MzY2NjE4LCJqdGkiOiI0MWY5NWJmMThjM2M0NTAzYjQyYjUyMzQxN2MyN2EwOCIsInVzZXJfaWQiOjN9.-QO0IJ87MYyGI25p28Drj5Aqx3PXyAJW_5zbSXq2Iu8"
  }
}
```
</details>

Essa parte do Backend foi criada usando um modelo de JWT (JSON Web Token) do Framework rest do Django.
A duração desse Token de autenticação pode ser configurada de acordo a atender as necessidades de segurança da plataforma.

#### Avaliar filme:  

Registra a avaliação de um filme.

<details> 
  <summary>PUT https://filmes-pra-ti.azurewebsites.net/posts/set_score_movie/ </summary>
   
```
headers
Authorization:Bearer <token_access>

body
{
    "movieId": "tt0092106",
    "score": "like" || "dislike" || "unscore"
}
```
```
response
{
  "status": "Succesful"
}
```
</details>

Nesse endpoint, não é necessário informar no corpo da requisição o usuário, pois o prório token é utilizado para gerir as informações de usuário.
Tal funcionalidade facilita a implementação de endpoints personalizados, uma vez que as informações sobre o usuário não precisam ser passadas, apenas o Token.

#### Recomendações:  

Recebe as recomendações para o usuário.

<details> 
  <summary>GET https://filmes-pra-ti.azurewebsites.net/posts/recommendations/ </summary>
   
```
headers
Authorization:Bearer <token_access>
```
```
response
{
  [
    {
        "recName": "Top Score 20",
        "recList": [
            {
                "title": "Toy Story",
                "poster": "https://m.media-amazon.com/images/M/MV5BMDU2ZWJlMjktMTRhMy00ZTA5LWEzNDgtYmNmZTEwZTViZWJkXkEyXkFqcGdeQXVyNDQ2OTk4MzI@._V1_QL75_UX190_CR0,1,190,281_.jpg",
                "minage": "G",
                "duration": "1h 21m",
                "year": "1995",
                "imdbScore": "8.3",
                "directors": "John Lasseter",
                "starActors": "Tom Hanks, Tim Allen, Don Rickles",
                "description": "A cowboy doll is profoundly threatened and jealous when a new spaceman action figure supplants him as top toy in a boy's bedroom.",
                "popularity": "653",
                "popularityDelta": "+110",
                "id": "tt0114709"
            },
            {
                "title": "Heat",
                "poster": "https://m.media-amazon.com/images/M/MV5BYjZjNTJlZGUtZTE1Ny00ZDc4LTgwYjUtMzk0NDgwYzZjYTk1XkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_QL75_UY281_CR3,0,190,281_.jpg",
                "minage": "R",
                "duration": "2h 50m",
                "year": "1995",
                "imdbScore": "8.3",
                "directors": "Michael Mann",
                "starActors": "Al Pacino, Robert De Niro, Val Kilmer",
                "description": "A group of high-end professional thieves start to feel the heat from the LAPD when they unknowingly leave a clue at their latest heist.",
                "popularity": "547",
                "popularityDelta": "-121",
                "id": "tt0113277"
            }
    },
    {
        "recName": "Top Popularity 20",
        "recList": [
            {
                "title": "Toy Story",
                "poster": "https://m.media-amazon.com/images/M/MV5BMDU2ZWJlMjktMTRhMy00ZTA5LWEzNDgtYmNmZTEwZTViZWJkXkEyXkFqcGdeQXVyNDQ2OTk4MzI@._V1_QL75_UX190_CR0,1,190,281_.jpg",
                "minage": "G",
                "duration": "1h 21m",
                "year": "1995",
                "imdbScore": "8.3",
                "directors": "John Lasseter",
                "starActors": "Tom Hanks, Tim Allen, Don Rickles",
                "description": "A cowboy doll is profoundly threatened and jealous when a new spaceman action figure supplants him as top toy in a boy's bedroom.",
                "popularity": "653",
                "popularityDelta": "+110",
                "id": "tt0114709"
            },
            {
                "title": "Jumanji",
                "poster": "https://m.media-amazon.com/images/M/MV5BZTk2ZmUwYmEtNTcwZS00YmMyLWFkYjMtNTRmZDA3YWExMjc2XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_QL75_UY281_CR11,0,190,281_.jpg",
                "minage": "PG",
                "duration": "1h 44m",
                "year": "1995",
                "imdbScore": "7.0",
                "directors": "Joe Johnston",
                "starActors": "Robin Williams, Kirsten Dunst, Bonnie Hunt",
                "description": "When two kids find and play a magical board game, they release a man trapped in it for decades - and a host of dangers that can only be stopped by finishing the game.",
                "popularity": "1111",
                "popularityDelta": "+269",
                "id": "tt0113497"
            }
    },
    {
        "recName": "Liked Movies",
        "recList": [
            {
                "title": "Toy Story",
                "poster": "https://m.media-amazon.com/images/M/MV5BMDU2ZWJlMjktMTRhMy00ZTA5LWEzNDgtYmNmZTEwZTViZWJkXkEyXkFqcGdeQXVyNDQ2OTk4MzI@._V1_QL75_UX190_CR0,1,190,281_.jpg",
                "minage": "G",
                "duration": "1h 21m",
                "year": "1995",
                "imdbScore": "8.3",
                "directors": "John Lasseter",
                "starActors": "Tom Hanks, Tim Allen, Don Rickles",
                "description": "A cowboy doll is profoundly threatened and jealous when a new spaceman action figure supplants him as top toy in a boy's bedroom.",
                "popularity": "653",
                "popularityDelta": "+110",
                "id": "tt0114709"
            },
            {
                "title": "The Transformers: The Movie",
                "poster": "https://m.media-amazon.com/images/M/MV5BZGM1MGY4OTYtOGZkOC00NjYyLTk3OTMtODUyZDdhYWQ3NGFjXkEyXkFqcGdeQXVyMzM4MjM0Nzg@._V1_QL75_UX190_CR0,4,190,281_.jpg",
                "minage": "PG",
                "duration": "1h 24m",
                "year": "1986",
                "imdbScore": "7.2",
                "directors": "Nelson Shin",
                "starActors": "Orson Welles, Robert Stack, Leonard Nimoy",
                "description": "The Autobots must stop a colossal planet consuming robot who goes after the Autobot Matrix of Leadership. At the same time, they must defend themselves against an all-out attack from the Dec... Read all",
                "id": "tt0092106"
            }
        ]
    }
  ]
}
```
</details>


#### Detalhes:  

Recebe detalhes de um filme obtidos através do web-scrapping.

<details> 
  <summary>GET https://filmes-pra-ti.azurewebsites.net/posts/movie_details/?movieId=movieId/ </summary>
   
```
headers
Authorization:Bearer <token_access>
```
```
response
{
  "title": "Toy Story",
  "poster": "https://m.media-amazon.com/images/M/MV5BMDU2ZWJlMjktMTRhMy00ZTA5LWEzNDgtYmNmZTEwZTViZWJkXkEyXkFqcGdeQXVyNDQ2OTk4MzI@._V1_QL75_UX190_CR0,1,190,281_.jpg",
  "minage": "G",
  "duration": "1h 21m",
  "year": "1995",
  "imdbScore": "8.3",
  "directors": "John Lasseter",
  "starActors": "Tom Hanks, Tim Allen, Don Rickles",
  "description": "A cowboy doll is profoundly threatened and jealous when a new spaceman action figure supplants him as top toy in a boy's bedroom.",
  "popularity": "653",
  "popularityDelta": "+110",
  "id": "tt0114709",
  "score": "like"
}
```
</details>

#### Busca:  

Realiza uma busca em quais desses filmes existem no dataset.

<details> 
  <summary>POST https://filmes-pra-ti.azurewebsites.net/posts/search/ </summary>
   
```
headers
Authorization:Bearer <token_access>

body
{
  "keySearch": "lord of"
}
```
```
[
  {
    "title": "Lord of the Flies",
    "poster": "https://m.media-amazon.com/images/M/MV5BM2FjM2VlYzgtYzI1OS00MTM2LWJmNjQtNTZkNTJjNzQzYzk5XkEyXkFqcGdeQXVyMzU4Nzk4MDI@._V1_QL75_UX190_CR0,4,190,281_.jpg",
    "minage": "Not Rated",
    "duration": "1h 32m",
    "year": "1963",
    "imdbScore": "6.9",
    "directors": "Peter Brook",
    "starActors": "James Aubrey, Tom Chapin, Hugh Edwards",
    "description": "Schoolboys marooned on a Pacific island create their own savage civilization.",
    "id": "tt0057261",
    "popularity": "0",
    "popularityDelta": "0"
  },
  {
    "title": "The Lord of the Rings: The Fellowship of the Ring",
    "poster": "https://m.media-amazon.com/images/M/MV5BN2EyZjM3NzUtNWUzMi00MTgxLWI0NTctMzY4M2VlOTdjZWRiXkEyXkFqcGdeQXVyNDUzOTQ5MjY@._V1_QL75_UX190_CR0,0,190,281_.jpg",
    "minage": "PG-13",
    "duration": "2h 58m",
    "year": "2001",
    "imdbScore": "8.8",
    "directors": "Peter Jackson",
    "starActors": "Elijah Wood, Ian McKellen, Orlando Bloom",
    "description": "A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron.",
    "popularity": "99",
    "popularityDelta": "-44",
    "id": "tt0120737"
  },
  {
    "title": "The Lord of the Rings: The Two Towers",
    "poster": "https://m.media-amazon.com/images/M/MV5BZGMxZTdjZmYtMmE2Ni00ZTdkLWI5NTgtNjlmMjBiNzU2MmI5XkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_QL75_UX190_CR0,7,190,281_.jpg",
    "minage": "PG-13",
    "duration": "2h 59m",
    "year": "2002",
    "imdbScore": "8.8",
    "directors": "Peter Jackson",
    "starActors": "Elijah Wood, Ian McKellen, Viggo Mortensen",
    "description": "While Frodo and Sam edge closer to Mordor with the help of the shifty Gollum, the divided fellowship makes a stand against Sauron's new ally, Saruman, and his hordes of Isengard.",
    "popularity": "385",
    "popularityDelta": "-140",
    "id": "tt0167261"
  },
  {
    "title": "The Lord of the Rings: The Return of the King",
    "poster": "https://m.media-amazon.com/images/M/MV5BNzA5ZDNlZWMtM2NhNS00NDJjLTk4NDItYTRmY2EwMWZlMTY3XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_QL75_UX190_CR0,0,190,281_.jpg",
    "minage": "PG-13",
    "duration": "3h 21m",
    "year": "2003",
    "imdbScore": "9.0",
    "directors": "Peter Jackson",
    "starActors": "Elijah Wood, Viggo Mortensen, Ian McKellen",
    "description": "Gandalf and Aragorn lead the World of Men against Sauron's army to draw his gaze from Frodo and Sam as they approach Mount Doom with the One Ring.",
    "popularity": "247",
    "popularityDelta": "-79",
    "id": "tt0167260"
  },
  {
    "title": "Lord of War",
    "poster": "https://m.media-amazon.com/images/M/MV5BMTYzZWE3MDAtZjZkMi00MzhlLTlhZDUtNmI2Zjg3OWVlZWI0XkEyXkFqcGdeQXVyNDk3NzU2MTQ@._V1_QL75_UX190_CR0,1,190,281_.jpg",
    "minage": "R",
    "duration": "2h 2m",
    "year": "2005",
    "imdbScore": "7.6",
    "directors": "Andrew Niccol",
    "starActors": "Nicolas Cage, Ethan Hawke, Jared Leto",
    "description": "An arms dealer confronts the morality of his work as he is being chased by an INTERPOL Agent.",
    "popularity": "2,910",
    "popularityDelta": "-66",
    "id": "tt0399295"
  },
  {
    "title": "Lord of Illusions",
    "poster": "https://m.media-amazon.com/images/M/MV5BNDg1OTc0MDQwNl5BMl5BanBnXkFtZTcwMjQ3NDk0NA@@._V1_QL75_UX190_CR0,2,190,281_.jpg",
    "minage": "R",
    "duration": "1h 49m",
    "year": "1995",
    "imdbScore": "6.0",
    "directors": "Clive Barker",
    "starActors": "Scott Bakula, Kevin J. O'Connor, J. Trevor Edmond",
    "description": "A private detective gets more than he bargains for when he encounters Philip Swan, a performer whose amazing illusions captivate the world, but they are not really what everyone thinks.",
    "id": "tt0113690",
    "popularity": "0",
    "popularityDelta": "0"
  },
  {
    "title": "The Lord of the Rings",
    "poster": "https://m.media-amazon.com/images/M/MV5BOGMyNWJhZmYtNGQxYi00Y2ZjLWJmNjktNTgzZWJjOTg4YjM3L2ltYWdlXkEyXkFqcGdeQXVyNTAyODkwOQ@@._V1_QL75_UX190_CR0,5,190,281_.jpg",
    "minage": "PG",
    "duration": "2h 12m",
    "year": "1978",
    "imdbScore": "6.2",
    "directors": "Ralph Bakshi",
    "starActors": "Christopher Guard, William Squire, Michael Scholes",
    "description": "The Fellowship of the Ring embark on a journey to destroy the One Ring and end Sauron's reign over Middle-earth.",
    "popularity": "3,450",
    "popularityDelta": "-548",
    "id": "tt0077869"
  }
]
```
</details>


#### Tecnologias, ferramentas, dependências, versões. etc. 

Para o desenvolvimento desse projeto foi utilizado o Django 4.0.4, em especial, o Django REST Framework 3.13.1 para implementação da API com os endpoints descritos. O deploy do back-end foi realizado em um App Service da Azure e o banco de dados foi o Azure SQL.

Outras bibliotecas e pacotes utilizados estão descritos no [requirements.txt](https://github.com/MC855FilmesParaTi/backend/blob/main/django_FPTI/requirements.txt)

#### Como executar

Para rodar o projeto localmente, dentro do diretório [django_FPTI](https://github.com/MC855FilmesParaTi/backend/tree/main/django_FPTI) executar:

```
python3 manage.py runserver
```

#### Trabalhos futuros

Carregar os filmes para o banco de dados também e desenvolver novos endpoints para novas funcionalidades.
Implementar amizades para recomendações a grupos de usuários, semelhante ao match do spotfy.
Sugestões de plataformas de streaming para assistir os conteúdos recomendados.
Integração com Machine Learning para garantir re-treinos dos sistemas de recomendação
Webscrapping sendo Atualizado automáticamente


