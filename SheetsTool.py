import datetime
import gspread
from gspread.utils import ValueRenderOption
import Util

class SheetsTool():
    
    def __init__(self, team: str, d: datetime.datetime, poster: str, task_id: int) -> None:
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
    
    def connect_to_google() -> gspread.Spreadsheet:
        """
        description: Creates Google API Client object
        return: Client object
        """
        return gspread.service_account(filename='docs\\bingobonanza-b9bddbaa451d.json').open_by_key('1NTA9T3I_zaln0foXbCULhw7WVzunyPbNfafpEjwnjiU')
    
    def update_sheets(self) -> None:
        """
        description: Updates bingo sheets
        return: None
        """
        # team, date, time, author
        sheet = SheetsTool.connect_to_google()
        worksheet = sheet.worksheet(self.team)
        # posted date
        worksheet.update_cell(self.task_id + 4, 7, self.d.strftime('%d-%b-%Y'))
        # posted time
        tz = datetime.timezone(datetime.timedelta(hours=-4.0), name="EST")
        worksheet.update_cell(self.task_id + 4, 8, self.d.astimezone(tz).strftime('%I:%M:%S %p'))
        # posted by
        worksheet.update_cell(self.task_id + 4, 9, self.poster)
        
        SheetsTool.update_master_sheet(self)
        
    def update_master_sheet(self) -> None:
        """
        description: Updates bingo master sheet
        return: None
        """
        sheet = SheetsTool.connect_to_google()
        worksheet = sheet.worksheet('Master')
        worksheet.update_cell(self.task_id + 4, Util.TEAMS_SHEETS_COLUMN_DICT.get(self.team), 'Complete')
        
    def add_purple(purple: str, team: str, date: str, time: str, player: str) -> None:
        """
        param str: name of the purple item
        param str: name of bingo team
        param str: date purple obtained per plugin
        param str: time purple obtained per plugin
        param str: name of player that obtained purple
        description: adds purple to Twisted Joe award table on sheet
        return: None
        """
        # 5 = Purple, 6 = Date, 7 = Time, 8 = Player
        sheet = SheetsTool.connect_to_google()
        worksheet = sheet.worksheet(team)
        values = ["", "", "", "", purple, date, time, player]
        worksheet.insert_row(values, index=71)
        formula = '=if(E71="","",E71&" - Obtained By: "&H71&" - On: "&F71&" - At: "&G71)'
        worksheet.update_acell("D71", formula)
