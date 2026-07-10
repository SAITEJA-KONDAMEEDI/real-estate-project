import os

import pymysql


class DataTier:

    def __init__(self):

        self.host = os.environ.get('DB_HOST', 'dbserversai.mysql.database.azure.com')

        self.user = os.environ.get('DB_USER', 'azsqladmin')

        self.password = os.environ.get('DB_PASS', 'Saiteja@2002')

        self.database = os.environ.get('DB_NAME', 'real_estate')


    def _get_connection(self):

        return pymysql.connect(

            host=self.host,

            user=self.user,

            password=self.password,

            database=self.database,

            ssl={'ssl': True}

        )


    def get_states(self):

        conn = self._get_connection()

        cursor = conn.cursor()

        cursor.execute("SELECT DISTINCT state FROM land_rates ORDER BY state")

        states = [row[0] for row in cursor.fetchall()]

        cursor.close()

        conn.close()

        return states


    def get_districts(self, state):

        conn = self._get_connection()

        cursor = conn.cursor()

        cursor.execute(

            "SELECT DISTINCT district FROM land_rates WHERE state=%s ORDER BY district",

            (state,)

        )

        districts = [row[0] for row in cursor.fetchall()]

        cursor.close()

        conn.close()

        return districts


    def get_mandals(self, state, district):

        conn = self._get_connection()

        cursor = conn.cursor()

        cursor.execute(

            "SELECT DISTINCT mandal FROM land_rates WHERE state=%s AND district=%s ORDER BY mandal",

            (state, district)

        )

        mandals = [row[0] for row in cursor.fetchall()]

        cursor.close()

        conn.close()

        return mandals


    def get_mandal_info(self, state, district, mandal):

        conn = self._get_connection()

        cursor = conn.cursor()

        cursor.execute(

            "SELECT rate_per_sq_yard, latitude, longitude FROM land_rates WHERE state=%s AND district=%s AND mandal=%s",

            (state, district, mandal)

        )

        result = cursor.fetchone()

        cursor.close()

        conn.close()

        return result
