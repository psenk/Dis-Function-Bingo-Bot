import datetime
import gspread
from utils import Constants, Functions

class SheetsTool():
    
    def __init__(self, team: str, d: datetime.datetime, poster: str, task_id: int = None, purple: str = None) -> None:
        """
        SheetsTool constructor
        param team: str - bingo team name
        param d: datetime of submission
        param poster: str - poster name
        param task_id: int - optional, bingo task id number
        param purple: str - optional, name of purple for bonus
        return: None
        """
        self.logger = Functions.create_logger("tools")
        self.team = team
        self.d = d
        self.poster = poster
        self.task_id = task_id
        self.purple = purple
    
    def connect_to_google(self) -> gspread.Spreadsheet:
        """
        Connects to Google API and returns bingo worksheet.
        return: GSpread Worksheet object
        """
        try:
            self.logger.info("Connecting to Google Sheets.")
            return gspread.service_account(filename='bingobonanza-b9bddbaa451d.json').open_by_key('1NTA9T3I_zaln0foXbCULhw7WVzunyPbNfafpEjwnjiU')
        except Exception as e:
            self.logger.error(f"Error connecting to Google Sheets: {e}", exc_info=True)
            raise
    
    def update_sheets(self) -> None:
        """
        Updates bingo sheets.
        return: None
        """
        try:
            # team, date, time, author
            book = self.connect_to_google(self)
            worksheet = book.worksheet(self.team)
            
            # posted date
            worksheet.update_cell(self.task_id + 4, 7, self.d.strftime('%d-%b-%Y'))
            # posted time
            tz = datetime.timezone(datetime.timedelta(hours=0), name="UTC")
            worksheet.update_cell(self.task_id + 4, 8, self.d.astimezone(tz).strftime('%H:%M'))
            # posted by
            worksheet.update_cell(self.task_id + 4, 9, self.poster)
            
            self.update_master_sheet(self)
            self.logger.info("update_sheets finished.")
        except Exception as e:
            self.logger.error(f"Error updating sheets: {e}", exc_info=True)
            raise
        
    def update_master_sheet(self) -> None:
        """
        Updates bingo master sheet
        return: None
        """
        try:
            book = self.connect_to_google(self)
            worksheet = book.worksheet('Master')
            worksheet.update_cell(self.task_id + 4, Constants.TEAMS_SHEETS_COLUMN_DICT.get(self.team), 'Complete')
            self.logger.info("update_master_sheet finished.")
        except Exception as e:
            self.logger.error(f"Error updating master sheet: {e}", exc_info=True)
            raise
        
    def add_purple(self, player: str) -> None:
        """
        Adds drop to Twisted Joe award table on sheet
        param player: str - name of player
        return: None
        """
        try:
            # 5 = Purple, 6 = Date, 7 = Time, 8 = Player
            book = self.connect_to_google(self)
            worksheet = book.worksheet(self.team)
            values = ["", "", "", "", self.purple, self.d.date().strftime('%d-%b-%Y'), self.d.time().strftime('%H:%M'), player]
            worksheet.insert_row(values, index=71)
            formula = '=if(E71="","",E71&" - Obtained By: "&H71&" - On: "&F71&" - At: "&G71)'
            worksheet.update_acell("D71", formula)
            self.logger.info("add_purple finished.")
        except Exception as e:
            self.logger.error(f"Error adding purple: {e}", exc_info=True)
            raise