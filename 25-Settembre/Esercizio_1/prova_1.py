# Scrivi una funzione slugify(text)

def slugify(text):
    """Converts a string to a slugified version.

    Args:
        text (str): The input string to be slugified.

    Returns:
        str: The slugified string, with spaces replaced by hyphens and all characters in lowercase.
    """
    return text.lower().replace(" ", "-")

def test_slugify():
    # Casi base
    assert slugify("Hello World") == "hello-world"
    assert slugify("Python 3.9") == "python-3.9"

    # Gestione di piu' spazi consecutivi (coerente con l'implementazione attuale)
    assert slugify("A  B") == "a--b"

    # Caratteri non alfabetici vengono preservati
    assert slugify("Ciao_mondo!") == "ciao_mondo!"

# Function for a internet research using ddgs, with verify=false for a ssl problems

from ddgs import DDGS

def internet_research(query):
    """
    Esegue una ricerca su Internet utilizzando DuckDuckGo Search (DDGS).

    Args:
        query (str): La stringa di ricerca da inviare a DuckDuckGo.

    Returns:
        list: Una lista di risultati di ricerca, dove ogni risultato è un dizionario contenente informazioni come titolo, descrizione e URL.

    Example:
        >>> results = internet_research("Python programming")
        >>> for result in results:
        ...     print(result["title"])
        Python (programming language) - Wikipedia
        Learn Python - Free Interactive Python Tutorial
        ...

    Note:
        La funzione utilizza `verify=False` per bypassare eventuali problemi SSL durante la richiesta.
    """
    results = []
    with DDGS(verify=False) as ddgs:
        for r in ddgs.text(query):
            results.append(r)
    return results

if __name__ == "__main__":
    print(slugify("Hello World"))
    print(internet_research("Python programming"))
