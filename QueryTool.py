import os
from datetime import datetime

import asyncpg
from dotenv import load_dotenv

load_dotenv(override=True)
import logging
import uuid

CONNECTION_STRING = os.getenv("PG_CONNECTION_STRING")

logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler(filename="logs/query_tool.log", encoding="utf-8", mode="w")])
logger = logging.getLogger(__name__)


class QueryTool:
    def __init__(self):
        self.pool = None

    async def __aenter__(self) -> "QueryTool":
        """
        Initializes connection pool when entering context (with statement)
        return: QueryTool Class instance
        """
        self.pool = await asyncpg.create_pool(dsn=CONNECTION_STRING, min_size=2, max_size=10)
        logger.info(f"QueryTool connection pool created.")
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        """
        Closes connection pool when exiting context (with statement)
        return: None
        """
        await self.pool.close()
        logger.info(f"QueryTool connection pool closed.")

    async def execute(self, query: str, *args) -> None:
        """
        Executes a database query without returning results.
        param query: str - SQL query
        param args: arguments for the SQL query
        return: None
        """
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    await connection.execute(query, *args)
            logger.info("Query executed successfully.")
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            raise

    async def fetch(self, query: str, *args) -> list:
        """
        Executes a query and returns multiple rows.
        param query: str - SQL query
        param args: arguments for the SQL query
        return: list - rows returned by the query
        """
        try:
            async with self.pool.acquire() as connection:
                return await connection.fetch(query, *args)
        except Exception as e:
            logger.error(f"Error fetching data: {e}")
            raise

    async def fetchval(self, query: str, *args) -> any:
        """
        Executes a query and returns a single value.
        param query: str - SQL query
        param args: arguments for the SQL query
        return: any - value returned by the query
        """
        try:
            async with self.pool.acquire() as connection:
                return await connection.fetchval(query, *args)
        except Exception as e:
            logger.error(f"Error fetching value: {e}")
            raise

    async def submit_task(self, player: str, team: str, uuid_no: uuid.UUID, jump_url: str, message_id: str, purple: str = None, task_id: int = None) -> None:
        """
        Stores bingo submission in the database.
        param player: str - name of bingo player
        param team: str - name of bingo team
        param uuid_no - UUID instance
        param jump_url - str - URL to submission
        param message_id: str - id of Discord submission post
        param purple: optional, item for bonus submission
        param task_id: optional, bingo task id
        return: None
        """
        d = datetime.now()
        query = "INSERT INTO submissions (task_id, player, team, uuid_no, jump_url, message_id, date_submitted, purple) VALUES ($1, $2, $3, $4, $5, $6, $7, $8);"
        await self.execute(query, task_id, player, team, uuid_no, jump_url, message_id, d, purple)
        logger.info("Task submitted.")

    async def delete_submission(self, uuid_no: uuid.UUID) -> None:
        """
        Deletes submission from database.
        param uuid_no: str - UUID of task
        return: None
        """
        query = "DELETE FROM submissions WHERE uuid_no = $1;"
        await self.execute(query, uuid_no)
        logger.info("Submission deleted.")

    async def get_submissions(self) -> list:
        """
        Retrieves all submissions from database.
        return: list - list of submissions
        """
        query = "SELECT * FROM submissions;"
        submissions = await self.fetch(query)
        logger.info("Submissions retrieved.")
        return submissions

    async def update_day(self, day: int) -> int:
        """
        Edit day of bingo in settings.
        param day: int - day of bingo
        return: int - day of bingo
        """
        query = "UPDATE settings SET bingo_day = $1;"
        await self.execute(query, day)
        logger.info("Bingo day updated.")
        return day

    async def get_day(self) -> int:
        """
        Retrieve day of bingo from settings.
        return: int - day of bingo
        """
        query = "SELECT bingo_day FROM settings;"
        day = await self.fetchval(query)
        logger.info("Retrieved bingo day.")
        return day

    # ? For future database growth

    async def get_teams(self) -> list:
        """
        Retrieve all teams + info from database.
        return: list - list of teams + info
        """
        query = "SELECT * FROM teams;"
        teams = await self.fetch(query)
        logger.info("Teams retrieved.")
        return teams

    async def get_team(self, team: str) -> list:
        """
        Retrieve specific team + info from database.
        param team: str - name of bingo team
        return: list - list of team + info
        """
        query = "SELECT * FROM teams WHERE team_name = $1;"
        teams = await self.fetch(query, team)
        logger.info("Team retrieved.")
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
        await self.execute(query, new_data, old_data, team)
        logger.info(f"Team info updated: {col} -> {new_data}")
