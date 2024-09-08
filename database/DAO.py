from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAnni():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct year(s.`datetime`) as anno
from new_ufo_sightings.sighting s 
order by anno desc """
            cursor.execute(query)

            for row in cursor:
                result.append(row["anno"])

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getForme(anno):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct s.shape as forma
from new_ufo_sightings.sighting s 
where year(s.`datetime`) = %s
order by forma asc  """
            cursor.execute(query,(anno,))

            for row in cursor:
                result.append(row["forma"])

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getNodi(anno,forma):

        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select *
                       from new_ufo_sightings.sighting s 
                       where s.shape = %s and year (s.`datetime`) = %s"""

            cursor.execute(query,(forma,anno))

            for row in cursor:
                result.append(Sighting(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getArchi(anno, forma,idmap):

        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select s.id as avvistamento1,s.longitude as lon1 , s2.id as avvistamento2, s2.longitude as lon2
from new_ufo_sightings.sighting s , new_ufo_sightings.sighting s2 
where s.id > s2.id and s.shape = %s and s.shape = s2.shape and 
year (s2.`datetime`) = %s and year (s2.`datetime`) = year(s.`datetime`) and 
s2.state = s.state and abs(s2.longitude) != abs(s.longitude)
order by lon1,lon2"""

            cursor.execute(query, (forma, anno))

            for row in cursor:
                avvistamento1 = idmap[row["avvistamento1"]]

                avvistamento2 = idmap[row["avvistamento2"]]

                result.append((avvistamento1,avvistamento2))

            cursor.close()
            cnx.close()
        return result