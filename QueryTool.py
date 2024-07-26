import os
from datetime import datetime

import asyncpg
from dotenv import load_dotenv

load_dotenv(override=True)
import uuid

CONNECTION_STRING = os.getenv("PG_CONNECTION_STRING")


class QueryTool:
    def __init__(self):
        self.pool = None

    async def __aenter__(self) -> None:
        """
        Initializes connection pool when entering context (with statement)
        return: None
        """
        self.pool = await asyncpg.create_pool(dsn=CONNECTION_STRING, min_size=2, max_size=2, max_inactive_connection_lifetime=10.0)
        print("Connection pool created.")
        return self

    async def __aexit__(self) -> None:
        """
        Closes connection pool when exiting context (with statement)
        """
        await self.pool.close()
        print("Connection pool closed.")

    async def submit_task(self, task_id: int, player: str, team: str, uuid_no: uuid.UUID, jump_url: str, message_id: int, purple: str = None) -> None:
        """
        Submits task for approval to the bingo admin team
        param int: id # of bingo task
        param str: name of player
        param str: name of bingo team
        param str: url to Discord submission post
        param int: id of Discord submission post
        param str: optional, item for bonus submission
        return: None
        """
        d = datetime.now()
        query = "INSERT INTO submissions (task_id, player, team, uuid, jump_url, message_id, date_submitted, purple) VALUES ($1, $2, $3, $4, $5, $6, $7, $8);"

        async with self.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(query, task_id, player, team, str(uuid_no), jump_url, message_id, d, purple)
        print("Task submitted, connection to database released.")

    async def delete_submission(self, uuid: str) -> None:
        """
        Deletes task from submissions table in database
        param str: uuid of task
        return: None
        """
        query = "DELETE FROM submissions WHERE uuid = $1;"

        async with self.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(query, uuid.strip())
        print("Submission deleted and connection released.")

    async def get_submissions(self) -> list:
        """
        Gets all submissions from database submissions table
        return: list of submissions
        """

        query = "SELECT * FROM submissions;"

        async with self.pool.acquire() as connection:
            submissions = await connection.fetch(query)
        print("Submissions retrieved and connection released.")
        return submissions

    async def update_day(self, day: int) -> int:
        """
        Update day of bingo
        param int: day of bingo
        return: int
        """
        query = "UPDATE settings SET bingo_day = $1;"

        async with self.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(query, day)
        print("Day of bingo updated and connection released.")
        return day

    async def get_day(self) -> int:
        """
        Get bingo day
        return int: bingo day
        """

        query = "SELECT bingo_day FROM settings;"

        async with self.pool.acquire() as connection:
            day = await connection.fetchval(query)
        print("Bingo day fetched and connection released.")
        return day


# OLD CODE
"""
        async def connect_to_db(task: str) -> asyncpg.Connection:
        param string: name of task being performed
        description: connects to the postgres database
        return: database connection object
        connection = await asyncpg.connect(CONNECTION_STRING)
        print(f"Connected to database for: {task}.")
        return connection
"""
