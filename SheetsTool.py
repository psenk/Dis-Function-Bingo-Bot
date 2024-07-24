import datetime
import gspread
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
    
    def connect_to_google() -> gspread.Client:
        """
        description: Creates Google API Client object
        return: Client object
        """
        return gspread.service_account(filename='docs\\bingobonanza-b9bddbaa451d.json')
    
    def update_sheets(self) -> None:
        """
        description: Updates bingo sheets
        return: None
        """
        # team, date, time, author
        gc = SheetsTool.connect_to_google()
        sheet = gc.open_by_key('1NTA9T3I_zaln0foXbCULhw7WVzunyPbNfafpEjwnjiU')
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
        gc = SheetsTool.connect_to_google()
        sheet = gc.open_by_key('1NTA9T3I_zaln0foXbCULhw7WVzunyPbNfafpEjwnjiU')
        worksheet = sheet.worksheet('Master')
        worksheet.update_cell(self.task_id + 4, Util.team_sheets_column_dict.get(self.team), 'Complete')