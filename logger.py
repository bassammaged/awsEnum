import logging
from os import path,remove
import colorama

class CustomError(Exception):
    '''
        Exception raise for error in the script.
        
        Arguments:
            - message: holds the error message
            - criticality_level: takes level of the error. 
            
            [NOTE: works based on log_action() function description].
            
        Returns:
            No returns.
    '''

    def __init__(self,criticality_level,message):
        '''
        Exception raise for error in the script.
        
        Arguments:
            - message: holds the error message
            - criticality_level: takes level of the error. 
            
            [NOTE: works based on log_action() function description].
            
        Returns:
            No returns.
    '''
        self.criticality_level  = criticality_level
        self.message            = message

class logit:
    '''
        logit class is created to log the actions and their serverities as well.
        
        Arguments:
            - message: holds the error message
            - criticality_level: takes level of the error. [NOTE: works based on log_action() function description].
            - verbose: verbosity status.
            - string target: target value to be used within the filename.
            
        Returns:
            No returns.
        Process:
            - logging the error message and level of criticality.
            - if the level of criticality is `c` or `e`, the script will be terminated.
    '''

    # ---- Static values
    log_action_firstrun = True  # using within _clear_old_logs
    working_dir = path.dirname(__file__)

    def __init__(self,profile,region,service_name,verbose=False):
        self.profile    = profile
        self.region     = region
        self.service    = service_name
        self.verbose    = verbose
        
        # -- Filepath
        self.fullpath           = path.join(path.dirname(__file__), 'logs', self.profile + '-' + self.region + '-' + self.service  + '.log')  
        
        # -- clear old logs related to the current enum process
        self._clear_old_logs()

    def _clear_old_logs(self):
        '''
            _clear_old_logs() is method to clear the *.log file that related to the target.
        '''
        if self.log_action_firstrun:
            if path.exists(self.fullpath):
                remove(self.fullpath)
            self.log_action_firstrun = False

    def add(self,criticality_level,message):
        '''
            add() is written to log the msg and severity of msg.
            Arguments:
                criticality_level: determine the level of log.
                - `d` for debug.
                - `i` for informative.
                - `w` for warning.
                - `e` for error.
                - `c` for critical.
                
                message: it holds the message that you want to log.
            Process:
                - logging the error message and level of criticality.
                - if the level of criticality is `c` or `e`, the script will be terminated.
        '''

        logging.basicConfig(filename=self.fullpath,encoding='utf-8',level=logging.DEBUG,format="%(levelname)s|%(asctime)s|%(message)s",datefmt='%m/%d/%Y %I:%M:%S %p')
        if criticality_level == 'd':
            logging.debug(message)
        elif criticality_level == 'w':
            logging.warning(message)
        elif criticality_level == 'e':
            logging.error(message)
        elif criticality_level == 'c':
            logging.critical(message)
        else:
            logging.info(message)

        # -- Checking the verbosity
        self._verbose(criticality_level,message)

        # -- terminate the script in error neither critical
        if criticality_level == 'c' or criticality_level == 'e':
            _terminator()

    def _verbose(self,criticality_level,message):
        '''
            _verbose() checks the virbosity status and print out the colored message if verbose was enabled.
        '''
        if self.verbose:
            sign = '\u0021'
            color = colorama.Fore.LIGHTBLUE_EX
            if criticality_level == 'd':
                sign = '>'
                color = colorama.Fore.LIGHTCYAN_EX
            if criticality_level == 'w':
                sign = '\u2622'
                color = colorama.Fore.YELLOW
            elif criticality_level == 'e':
                sign = '\u2718'
                color = colorama.Fore.LIGHTRED_EX
            elif criticality_level == 'c':
                sign = '\u2718'
                color = colorama.Fore.RED
            elif criticality_level == 'f':
                sign = '\u2714'
                color = colorama.Fore.GREEN

            print(color + '[' + sign + '] ' + message + colorama.Style.RESET_ALL)

class _terminator():
    '''
        terminator class is written to be used by `log_it` class to terminate the script incase of the level of logging is `c` either `e`.
    '''
    def __init__(self):
        exit()