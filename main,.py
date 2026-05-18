import requests


class Livro:
    def __init__(self, titulo, autor, ano):
        self.titulo = titulo
        self.autor = autor
        self.ano = ano

    def __str__(self):
        return f"{self.titulo} - {self.autor} ({self.ano})"


class Biblioteca:
    def __init__(self):
        self.livros = []

    def adicionar_livro(self, livro):
        self.livros.append(livro)
        print("Livro adicionado!")

    def listar_livros(self):
        if not self.livros:
            print("Nenhum livro adicionado.")
            return

        print("\n===== LISTA DE LIVROS =====")

        for i, livro in enumerate(self.livros, start=1):
            print(f"{i}. {livro}")

    def buscar_livro(self, titulo):
        encontrados = [
            l for l in self.livros
            if titulo.lower() in l.titulo.lower()
        ]

        if not encontrados:
            print("Nenhum livro encontrado.")
        else:
            print("\n===== RESULTADOS =====")

            for livro in encontrados:
                print(livro)

    def remover_livro(self, titulo):
        for livro in self.livros:
            if livro.titulo.lower() == titulo.lower():
                self.livros.remove(livro)
                print("Livro removido!")
                return

        print("Livro não encontrado.")


def buscar_livro_api(titulo):
    url = "https://www.googleapis.com/books/v1/volumes"

    params = {
        "q": titulo,
        "maxResults": 1
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("Erro ao acessar API.")
        return None

    dados = response.json()

    if "items" not in dados:
        print("Livro não encontrado na API.")
        return None

    info = dados["items"][0]["volumeInfo"]

    titulo = info.get("title", "Desconhecido")

    autores = info.get("authors", ["Desconhecido"])
    autor = ", ".join(autores)

    ano = info.get("publishedDate", "Desconhecido")

    return Livro(titulo, autor, ano)


def menu():
    biblioteca = Biblioteca()

    while True:
        print("\n===== BIBLIOTECA =====")
        print("1 - Adicionar Livro")
        print("2 - Listar Livros")
        print("3 - Buscar Livro")
        print("4 - Remover Livro")
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            titulo = input("Digite o título: ")

            livro = buscar_livro_api(titulo)

            if livro:
                print("\nLivro encontrado:")
                print(livro)

                confirmar = input("Adicionar? (s/n): ")

                if confirmar.lower() == "s":
                    biblioteca.adicionar_livro(livro)

        elif opcao == "2":
            biblioteca.listar_livros()

        elif opcao == "3":
            titulo = input("Digite um título: ")
            biblioteca.buscar_livro(titulo)

        elif opcao == "4":
            titulo = input("Digite o título: ")
            biblioteca.remover_livro(titulo)

        elif opcao == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida.")


menu()