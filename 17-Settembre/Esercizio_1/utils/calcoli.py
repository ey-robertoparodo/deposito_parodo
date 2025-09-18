def somma(a: int, b: int) -> int:
    """
    Somma di due numeri interi.

    Parameters
    ----------

    a : int
            Primo numero intero.

    b : int
            Secondo numero intero.

    Returns
    -------
    int

        La somma di due numeri interi.

    """
    return a + b


def words_count(sentece: str) -> int:
    """
    Calcola quante lettere sono presenti in una parola o frase.

    Parameters
    ----------

    sentece : str
             Parola o frase.

    Returns
    -------
    int

        Il totale delle lettere presenti nella parola o frase.

    """
    return len(sentece.replace(" ", ""))


def conta_unici(lista):
    """
    Restituisce il numero degli elementi unici presenti all'interno della lista.

    Parameters
    ----------

    lista : list
            Lista di elementi.

    Returns
    -------
    int

        Il totale degli elementi unici presenti all'interno della lista.

    """
    return len(set(lista))


def primo_fino_a_n(n):
    """
    Restituisce una lista contenenti i numero primi dell'intervallo 1 a n.

    Parameters
    ----------

    n : int
        Rapprenseta il limite finale dell'intervallo.

    Returns
    -------
    list

        La lista dei numeri primi che vanno da 1 a n.

    """
    c = []
    return c
