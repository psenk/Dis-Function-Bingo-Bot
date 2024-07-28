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

    async def __aenter__(self) -> "QueryTool":
        """
        Initializes connection pool when entering context (with statement)
        return: QueryTool Class instance
        """
        self.pool = await asyncpg.create_pool(dsn=CONNECTION_STRING, min_size=2, max_size=10)
        print("Pool created.")
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        """
        Closes connection pool when exiting context (with statement)
        return: None
        """
        await self.pool.close()
        print("Pool closed.")

    async def submit_task(self, player: str, team: str, uuid_no: uuid.UUID, jump_url: str, message_id: str, purple: str = None, task_id: int = None) -> None:
        """
        Stores bingo submission in the database.
        param player: str - name of bingo player
        param team: str - name of bingo team
        param uuid_no - UUID instance
        param jump_url - str - URL to submission # ! CAN THIS BE REPLACED WITH MESSAGE_ID?
        param message_id: str - id of Discord submission post
        param purple: optional, item for bonus submission
        param task_id: optional, bingo task id
        return: None
        """
        d = datetime.now()
        query = "INSERT INTO submissions (task_id, player, team, uuid, jump_url, message_id, date_submitted, purple) VALUES ($1, $2, $3, $4, $5, $6, $7, $8);"

        async with self.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(query, task_id, player, team, str(uuid_no), jump_url, message_id, d, purple)
        print("Task submitted, connection closed.")

    async def delete_submission(self, uuid: str) -> None:
        """
        Deletes submission from database.
        param uuid: str - UUID of task
        return: None
        """
        query = "DELETE FROM submissions WHERE uuid = $1;"

        async with self.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(query, uuid.strip())
        print("Submission deleted, connection closed.")

    async def get_submissions(self) -> list:
        """
        Retrieves all submissions from database.
        return: list - list of submissions
        """

        query = "SELECT * FROM submissions;"

        async with self.pool.acquire() as connection:
            submissions = await connection.fetch(query)
        print("Submissions retrieved, connection closed.")
        return submissions

    async def update_day(self, day: int) -> int:
        """
        Edit day of bingo in settings.
        param day: int - day of bingo
        return: int - day of bingo
        """
        query = "UPDATE settings SET bingo_day = $1;"

        async with self.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(query, day)
        print("Bingo day updated, connection closed.")
        return day

    async def get_day(self) -> int:
        """
        Retrieve day of bingo from settings.
        return: int - day of bingo
        """

        query = "SELECT bingo_day FROM settings;"

        async with self.pool.acquire() as connection:
            day = await connection.fetchval(query)
        print("Retrieved bingo day, connection closed.")
        return day

    # ? For future database growth

    async def get_teams(self) -> list:
        """
        Retrieve all teams + info from database.
        return: list - list of teams + info
        """

        query = "SELECT * FROM teams;"

        async with self.pool.acquire() as connection:
            teams = await connection.fetch(query)
        print("Teams retrieved, connection closed.")
        return teams

    async def get_team(self, team: str) -> list:
        """
        Retrieve specific team + info from database.
        param team: str - name of bingo team
        return: list - list of team + info
        """

        query = "SELECT * FROM teams WHERE team_name = $1;"

        async with self.pool.acquire() as connection:
            teams = await connection.fetch(query, team)
        print("Team retrieved, connection closed.")
        return teams

    async def update_team_info(self, team: str, col: str, old_data: str, new_data: str) -> None:
        """
        Update team + info in database.
        param team: str - name of bingo team
        param col: str - name of column on sheet
        param old_data: str - old team info
        param new_data: str - new team info
        return: None
        """
        query = f"UPDATE teams SET {col} = $1 WHERE {col} = $2 AND team_name = $3;"
        print(f"Col: {col}")
        print(f"Old data: {old_data}, New data: {new_data}")
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(query, new_data, old_data, team)
        print(f"Team record updated: {col} -> {new_data}")
