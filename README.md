# API-de-X

#Utilizamos " client.search_tweet(QUERY, product='Top')" 
-> "TOP"=solo devuelve los tweets más destacados dentro del rango de fechas, 
            pero es posible que los tweets destacados que encuentres sean de un solo día porque son los más populares en ese rango.
-> "RECENT"=Devuelve los tweets más recientes que coinciden con la consulta. Se limita a 
            tweets publicados en los últimos 7 días.
->"FULLARCHIVE"=Proporciona acceso a todos los tweets que coincidan con la consulta, sin 
                limitaciones de fecha. Te permite acceder a tweets históricos desde el inicio de Twitter.