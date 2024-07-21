import asyncpg
import os
import datetime
from dotenv import load_dotenv
load_dotenv(override=True)

CONNECTION_STRING = os.getenv("PG_CONNECTION_STRING")

class QueryTool():
    
    def __init__(self):
        super().__init__(timeout=None)
    
    async def connect_to_db(task: str) -> asyncpg.Connection:
        """
        param string: name of task being performed
        description: connects to the postgres database
        return: database connection object
        """
        connection = await asyncpg.connect(CONNECTION_STRING)
        print(f"Connected to database for: {task}.")
        return connection
    
    # Sends task to submissions table
    async def submit_task(task_id: int, player: str, team: str, jump_url: str, message_id: int) -> None:
        """
        param int: id # of bingo task
        param str: name of player
        param str: name of bingo team
        param str: url to Discord submission post
        param int: id of Discord submission post
        description: submits bingo task for approval to the bingo admins
        return: None
        """
        connection = await QueryTool.connect_to_db("task submission")
        d = datetime.datetime.now()
        query = f"INSERT INTO submissions (task_id, player, team, jump_url, message_id, date_submitted) VALUES ({task_id}, '{player}', '{team}', '{jump_url}', {message_id}, '{d}');"
        
        await connection.execute(query)
        await connection.close()
        print("Database connection closed.")
        
    # Deletes task
    async def delete_submission(task_id: int, team: str) -> None:
        """
        param int: id # of bingo task
        param str: name of bingo team
        description: delete task from submissions table
        return: None
        """
        connection = await QueryTool.connect_to_db("submission deletion")
        query = f"DELETE FROM submissions WHERE task_id = {task_id} AND team = '{team}'"
        
        await connection.execute(query)
        await connection.close()
        print("Database connection closed.")
    
    async def reject() -> None:
        pass
    
    async def get_submissions() -> list:
        """
        description: gets all submissions from database submissions table
        return: list of submissions
        """
        connection = await QueryTool.connect_to_db("get submissions")    
        tx = connection.transaction()
        await tx.start()
        try:
            query = f"SELECT * FROM submissions;"
            cursor = await connection.cursor(query)
            return_list = await cursor.fetch(100)
        except:
            await tx.rollback()
            print("EXCEPTION: get_submissions")
        else:
            await tx.commit()
                  
        await connection.close()
        print("Database connection closed.")
        return return_list