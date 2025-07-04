# SpeedGarage – Backend

SpeedGarage é uma aplicação web que permite usuários escreverem críticas de carros icônicos, tanto da vida real quanto do mundo dos filmes, séries e animes. O projeto é baseado no escopo original da aplicação **Minha Crítica**, que teria como proposta avaliar obras como filmes, séries e livros, onde foi adaptado para veículos memoráveis.

---

## Proposta

Inspirado em plataformas como [IMDb](https://www.imdb.com/) e [Rotten Tomatoes](https://www.rottentomatoes.com/), o SpeedGarage permite que usuários:

- Façam login e cadastro
- Naveguem por críticas públicas
- Criem e editem críticas
- Curtam avaliações de outros usuários
- Visualizem médias de avaliações por carro
- Enviem imagens (motor, interior, exterior) de cada carro
- Descubram os carros mais bem avaliados

---

## Deploy

| Ambiente | URL |
|----------|-----|
| **Backend (Railway)** | https://speedgarage-backend.up.railway.app |
| **Frontend (Vercel)** | https://speedgarage-frontend.vercel.app |

---

## Tecnologias

- **Django 5.2.2**
- **Django REST Framework**
- **JWT (Autenticação via SimpleJWT)**
- **PostgreSQL** (Railway)
- **Cloudinary** (armazenamento de imagens)
- **Railway** (infraestrutura backend)
- **Vercel** (frontend Angular)

---

## Endpoints Principais

### Autenticação

| Rota | Descrição |
|------|-----------|
| `POST /register/` | Registro de novo usuário |
| `POST /token/` | Login com JWT (usuário ou e-mail) |
| `POST /token/refresh/` | Renovação de token |

### Carros

| Rota | Descrição |
|------|-----------|
| `GET /api/cars/` | Listar todos os carros |
| `POST /api/cars/` | Criar um novo carro |
| `GET /api/cars/top?n=3` | Carros com maior média |
| `GET /api/cars/marcas/` | Listar marcas distintas |
| `GET /api/cars/modelos/?marca=` | Modelos da marca |
| `GET /api/cars/anos/?marca=&modelo=` | Anos disponíveis |

### Críticas

| Rota | Descrição |
|------|-----------|
| `GET /api/reviews/` | Lista todas as críticas públicas |
| `POST /api/reviews/` | Cria uma nova crítica |
| `PUT /api/reviews/{id}/` | Atualiza crítica (se autor) |
| `DELETE /api/reviews/{id}/` | Remove crítica (se autor) |
| `POST /api/reviews/{id}/like/` | Dá like em uma crítica |
| `POST /api/reviews/{id}/unlike/` | Remove like da crítica |

### Imagens

| Rota | Descrição |
|------|-----------|
| `GET /api/car-images/` | Lista imagens enviadas |
| `POST /api/car-images/` | Envia imagem para carro |
| `DELETE /api/car-images/{id}/` | Deleta imagem enviada |

---

## Exemplo de resposta de carro

```json
{
  "id": 1,
  "marca": "Fiat",
  "modelo": "Uno Mille",
  "ano": 2005,
  "media_avaliacao": 4.9,
  "imagens": [
    "https://res.cloudinary.com/.../uno_exterior.jpg",
    "https://res.cloudinary.com/.../uno_motor.jpg"
  ]
}
```
## Variáveis de Ambiente (Railway)

| Variável                | Descrição                               |
| ----------------------- | --------------------------------------- |
| `DJANGO_SECRET_KEY`     | Chave secreta da aplicação              |
| `DEBUG`                 | `False` em produção                     |
| `ALLOWED_HOSTS`         | `.up.railway.app, localhost, 127.0.0.1` |
| `CLOUDINARY_CLOUD_NAME` | Nome da conta Cloudinary                |
| `CLOUDINARY_API_KEY`    | Chave da API Cloudinary                 |
| `CLOUDINARY_API_SECRET` | Segredo da API Cloudinary               |

## Como Rodar Localmente

```
# Clone o projeto
git clone https://github.com/seu-usuario/speedgarage-backend.git
cd speedgarage-backend

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt

# Crie o banco local
python manage.py migrate

# Crie superusuário (opcional)
python manage.py createsuperuser

# Rode a aplicação
python manage.py runserver

```

## Funcionalidades Implementadas
 - Login e registro com username ou email
 - Upload de imagens para Cloudinary
 - Sistema de likes por crítica
 - Criação e edição de críticas autenticadas
 - Visualização e busca de carros
 - Top N carros mais bem avaliados
 - Filtro de marca, modelo e ano
 - Integração com frontend Angular via Vercel

## Equipe
Backend: @pedr0alencar

Frontend base: @leonardo-vargas-de-paula

