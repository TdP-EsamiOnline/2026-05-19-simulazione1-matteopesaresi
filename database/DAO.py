from database.DB_connect import DBConnect
from model.artista import Artista




class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_artisti():
        cnx = DBConnect.get_connection()
        if cnx is None:
            print(f"Errore di connessione!")
            return
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("select * from Artist")
        risultato = []
        for row in cursor:
            risultato.append(Artista(**row))
        cursor.close()
        cnx.close()
        return risultato

    @staticmethod
    def get_artist_track(genere):
        cnx = DBConnect.get_connection()
        if cnx is None:
            print(f"Errore di connessione!")
            return
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("SELECT a.ArtistId, a.Name, i.CustomerId, il.Quantity FROM Artist a, Album al, Track tr, Genre gen, InvoiceLine il, Invoice i WHERE a.ArtistId = al.ArtistId AND al.AlbumId = tr.AlbumId AND tr.GenreId = gen.GenreId AND il.TrackId = tr.TrackId AND il.InvoiceId = i.InvoiceId AND gen.Name = %s",(genere,))
        risultato = []
        for row in cursor:
            risultato.append({
                "id": row["ArtistId"],
                "customer": row["CustomerId"],
                "qt": row["Quantity"]
            })
        cursor.close()
        cnx.close()
        return risultato

    @staticmethod
    def get_generi():
        cnx = DBConnect.get_connection()
        if cnx is None:
            print(f"Errore di connessione!")
            return
        risultato = []
        cursor = cnx.cursor()
        cursor.execute("select * from Genre")
        for row in cursor:
            risultato.append(row[1])
        cursor.close()
        cnx.close()
        return risultato

    @staticmethod
    def get_vertici(genere_nome):
        # Serve per prendere i nodi esatti (tutti gli artisti di quel genere, anche senza vendite)
        cnx = DBConnect.get_connection()
        if cnx is None:
            return []
        cursor = cnx.cursor(dictionary=True)
        query = """
            SELECT DISTINCT a.ArtistId, a.Name
            FROM Artist a
            JOIN Album al ON a.ArtistId = al.ArtistId
            JOIN Track t ON al.AlbumId = t.AlbumId
            JOIN Genre g ON t.GenreId = g.GenreId
            WHERE g.Name = %s
            """
        cursor.execute(query, (genere_nome,))
        risultato = []
        for row in cursor:
            risultato.append(row["ArtistId"])  # o ritorniamo l'oggetto, per ora l'ID basta e avanza
        cursor.close()
        cnx.close()
        return risultato

