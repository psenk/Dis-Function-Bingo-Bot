import datetime
import gspread
import Util

class SheetsTool():
    
    def __init__(self, team: str, d: datetime.datetime, poster: str, task_id: int = None, purple: str = None) -> None:
        """
        param string: bingo team name
        param datetime: timestamp of submission
        param string: poster of submission
        param int: bingo task number
        description: Constructor for SheetsTool
        return: None
        """
        self.team = team
        self.d = d
        self.poster = poster
        self.task_id = task_id
        self.purple = purple
    
    def connect_to_google() -> gspread.Spreadsheet:
        """
        Creates Google API Client object
        return: Client object
        """
        return gspread.service_account(filename='bingobonanza-b9bddbaa451d.json').open_by_key('1NTA9T3I_zaln0foXbCULhw7WVzunyPbNfafpEjwnjiU')
    
    def update_sheets(self) -> None:
        """
        Updates bingo sheets.
        return: None
        """
        # team, date, time, author
        book = SheetsTool.connect_to_google()
        worksheet = book.worksheet(self.team)
        # posted date
        worksheet.update_cell(self.task_id + 4, 7, self.d.strftime('%d-%b-%Y'))
        # posted time
        tz = datetime.timezone(datetime.timedelta(hours=0), name="UTC")
        worksheet.update_cell(self.task_id + 4, 8, self.d.astimezone(tz).strftime('%H:%M'))
        # posted by
        worksheet.update_cell(self.task_id + 4, 9, self.poster)
        
        SheetsTool.update_master_sheet(self)
        
    def update_master_sheet(self) -> None:
        """
        Updates bingo master sheet
        return: None
        """
        book = SheetsTool.connect_to_google()
        worksheet = book.worksheet('Master')
        worksheet.update_cell(self.task_id + 4, Util.TEAMS_SHEETS_COLUMN_DICT.get(self.team), 'Complete')
        
    def add_purple(self, player: str) -> None:
        """
        Adds drop to Twisted Joe award table on sheet
        param player: str - name of player
        return: None
        """
        # 5 = Purple, 6 = Date, 7 = Time, 8 = Player
        book = SheetsTool.connect_to_google()
        worksheet = book.worksheet(self.team)
        values = ["", "", "", "", self.purple, self.d.date().strftime('%d-%b-%Y'), self.d.time().strftime('%H:%M'), player]
        worksheet.insert_row(values, index=71)
        formula = '=if(E71="","",E71&" - Obtained By: "&H71&" - On: "&F71&" - At: "&G71)'
        worksheet.update_acell("D71", formula)
