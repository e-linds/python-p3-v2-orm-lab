from __init__ import CURSOR, CONN
from department import Department
from employee import Employee


class Review:

    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, year, summary, employee_id, id=None):
        self.id = id
        self.year = year
        self.summary = summary
        self.employee_id = employee_id

    def __repr__(self):
        return (
            f"<Review {self.id}: {self.year}, {self.summary}, "
            + f"Employee: {self.employee_id}>"
        )

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Review instances """
        sql = """
            CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY,
            year INT,
            summary TEXT,
            employee_id INTEGER,
            FOREIGN KEY (employee_id) REFERENCES employee(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Review  instances """
        sql = """
            DROP TABLE IF EXISTS reviews;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        sql = f'''
            INSERT INTO reviews(year, summary, employee_id)
            VALUES ({self.year}, "{self.summary}", {self.employee_id});
            
        '''
        CURSOR.execute(sql)
        CONN.commit()

        newid = CURSOR.execute(''' SELECT * FROM reviews;''').fetchall()[-1][0]

        self.id = newid
       
            

    @classmethod
    def create(cls, year, summary, employee_id):
        newinstance = Review(year, summary, employee_id)
        newinstance.save()
        return newinstance
        
   
    @classmethod
    def instance_from_db(cls, row):

        sql = CURSOR.execute(f""" 
            SELECT * FROM reviews
            WHERE id = {row[0]}
        """).fetchone()
        if sql:
            return Review(id = sql[0], year = sql[1], summary = sql[2], employee_id = sql[3])
        else: 
            return Review.create(row[0], row[1], row[2], row[3])

     
   
    @classmethod
    def find_by_id(cls, id):
        sql = CURSOR.execute(f""" 
            SELECT * FROM reviews
            WHERE id = {id};
        """).fetchone()
        if sql:
            return Review(id = sql[0], year = sql[1], summary = sql[2], employee_id = sql[3])
        else: return None
        
    def update(self):
        sql = f'''
        UPDATE reviews 
        SET year = {self.year}, summary = "{self.summary}", employee_id = {self.employee_id} 
        WHERE id = {self.id};
        '''
        CURSOR.execute(sql).fetchall()
        CONN.commit()


    def delete(self):
        sql = f'''
            DELETE FROM reviews
            WHERE id = {self.id};
        '''
        CURSOR.execute(sql)
        CONN.commit()
        
        self.id = None
                

    @classmethod
    def get_all(cls):
        all_reviews = CURSOR.execute('''
        SELECT * FROM reviews
        ''').fetchall()
        array = []
        for each in all_reviews:
            array.append(Review(id = each[0],
                                year = each[1],
                                summary = each[2],
                                employee_id = each[3]))
        return array
    

    def get_year(self):
        return self._year

    def set_year(self, value):
        if type(value) is int and value >= 2000:
            self._year = value
        else: raise ValueError("not valid year")
    
    year = property(get_year, set_year)

    def get_summary(self):
        return self._summary

    def set_summary(self, value):
        if type(value) is str and len(value) > 0:
            self._summary = value
        else: raise ValueError("not valid summary")
    
    summary = property(get_summary, set_summary)

    #idk what is going on here below 

    def get_employee_id(self):
        return self._employee_id
        
    def set_employee_id(self, value):
        employee = Employee.find_by_id(value)
        if type(employee) is Employee:
            self._employee_id = value
        else: raise ValueError("not valid Employee type")

    employee_id = property(get_employee_id, set_employee_id)

