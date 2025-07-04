validCommandTable = {
                     # System commands
                     '*IDN?': [],
                     '*RST': [],
                     '*CLR': [],
                     '*TST?': [],
                     '*HLP': [],

                     # SYSTem Subtree
                     'SYST:DAC': [['int', 0, 4059]],
                     'SYST:ID': [],
                     'SYST:VERS': [],
                     'SYST:MODE:LOW:IN': [],
                     'SYST:MODE:HIGH:IN': [],
                     'SYST:MODE:LOW:OUT': [],
                     'SYST:MODE:HIGH:OUT': [],
                     'SYST:VBAT': [],
                     'SYST:SAVE': [['int', 0, 4]],
                     'SYST:SCONF': [],
                     'SYST:TCAL': [],
                     'SYST:TTEST': [],
                     'SYST:THRE': [],
                     'SYST:STEST': [],
                     'SYST:OFFS': [['int', 0, 4095]],
                     'SYST:CLRCONF': [],

                     # FREQuency Subsystem
                     'FREQ:START': [['int', 0, 6000000000]],
                     'FREQ:STOP': [['int', 0, 6000000000]],
                     'FREQ:CENT': [['int', 0, 6000000000]],
                     'FREQ:SPAN': [['int', 0, 290]],
                     'FREQ:SPAN:ZERO': [],
                     'FREQ:RBW': [['str', '3', '10', '30', '100', '300', '600']],
                     'FREQ:RBW:AUTO': [],
                     'FREQ:DUMP': [],

                     'FREQ:SCAN:FREQ': [['int', 0, 6000000000], ['int', 0, 6000000000]],
                     'FREQ:SCAN:MEAS': [['int', 0, 6000000000], ['int', 0, 6000000000]],
                     'FREQ:SCAN:STOR': [['int', 0, 6000000000], ['int', 0, 6000000000]],

                     'FREQ:IF:AUTO': [],
                     'FREQ:IF': [['int', 433000000, 435000000]],
                     'FREQ:IF1': [['int', 800000000, 800000000]],

                     # LeVeL Subsystem
                     'LVL:ATT': [['int', 0, 31]],
                     'LVL:ATT:AUTO': [],
                     'LVL:REF': [['float', float('-inf'), float('inf')]],
                     'LVL:REF:AUTO': [],
                     'LVL:SCAL': [['str', '1', '2', '5', '10', '20']],
                     'LVL:SCAL:AUTO': [],
                     'LVL:UNIT': [['str', 'dBm', 'dBmV', 'dBuV', 'V', 'W']],
                     'LVL:XGAIN': [['int', -100, 100]],
                     'LVL:LNA:ON': [],
                     'LVL:LNA:OFF': [],

                     # TRIGger Subsystem
                     'TRIG:TYPE:AUTO': [],
                     'TRIG:TYPE:NORM': [],
                     'TRIG:TYPE:SNGL': [],
                     'TRIG:LVL': [['float', -200.0, 13.0]],

                     # TRACe Subsystem
                     'TRAC:FREZ:ON': [['int', 1, 4]],
                     'TRAC:FREZ:OFF': [['int', 1, 4]],
                     'TRAC:VIEW:ON': [['int', 1, 4]],
                     'TRAC:VIEW:OFF': [['int', 1, 4]],
                     'TRAC:VAL': [['int', 1, 4]],
                     'TRAC:COPY': [['int', 1, 4], ['int', 1, 4]],
                     'TRAC:SUB': [['int', 1, 4], ['int', 1, 4]],
                     'TRAC:SUB:OFF': [['int', 1, 4]],

                     # DISPlay Subsystem
                     'DISP:PAUSE': [],
                     'DISP:RESUME': [],
                     'DISP:REFRESH': [],
                     'DISP:COLOR': [['int', 0, 30], ['hex', 0x0, 0xffffff]],
                     'DISP:SWEEPTIME': [['int', 0, 10]],
                     'DISP:SPUR': [['bool']],
                     'DISP:CAPT': [],

                     # OUTput Subsystem
                     'OUT:LEV': [['int', -76, 13]],
                     'OUT:LEVO:LOW': [['int', -70, 70]],
                     'OUT:LEVO:HIGH': [['int', -70, 70]],
                     'OUT:LEVO:SWIT': [['int', -70, 70]],
                     'OUT:LEVO:LNA': [['int', -70, 70]],
                     'OUT:LEVCH': [['int', -70, 70]],
                     'OUT:MOD': [['str', 'off', 'am', 'nfm', 'wfm', 'extern']],
                     'OUT:MOD:FREQ': [['int', 100, 6000]],
                     'OUT:ON': [],
                     'OUT:OFF': [],
                     'OUT:CALI:OFF': [],
                     'OUT:CALI': [['str', '30', '15', '10', '4', '3', '2', '1']],
                     'OUT:EXTGN': [['int', -100, 100]],

                     # MARKer Subsystem
                     'MARK:ON': [['int', 1, 8]],
                     'MARK:NOIS:SET': [['int', 1, 8]],
                     'MARK:NOIS:OFF': [['int', 1, 8]],
                     'MARK:TRAKING': [['int', 1, 8]],
                     'MARK:FREQ': [['int', 1, 8], ['int', 0, 6000000000]],

                     'MARK:DELT': [['int', 1, 8], ['int', 1, 8]],
                     'MARK:DELT:OFF': [['int', 1, 8]],

                     'MARK:TRAK:SET': [['int', 1, 8]],
                     'MARK:TRAK:OFF': [['int', 1, 8]],

                     'MARK:TRAC': [['int', 1, 8], ['int', 1, 4]],

                     'MARK:AVER:SET': [['int', 1, 8]],
                     'MARK:AVER:OFF': [['int', 1, 8]],

                     'MARK:SRCH:PEAK': [['int', 1, 8]],

                     'MARK:SRCH:MINR': [['int', 1, 8]],
                     'MARK:SRCH:MINL': [['int', 1, 8]],
                     'MARK:SRCH:MAXR': [['int', 1, 8]],
                     'MARK:SRCH:MAXL': [['int', 1, 8]],

                     'MARK:FREQ': [['int', 1, 8], ['int', 0, 6000000000]],
                     'MARK:DEL': [['int', 1, 8]],
                     'MARK:RST': [],

                     'MARK:DIFF': [['int', 1, 8], ['int', 1, 8]],
                     'MARK:DIFF:OFF': [['int', 1, 8]],

                     # MEASure Subsystem
                    'MEAS:OFF': [],
                    'MEAS:DUMP': [['int', 0, 2]],
                    'MEAS:HARM': [['int', 0, 6000000000], ['int', 0, 6000000000]],
                    'MEAS:OIP3': [['int', 0, 6000000000], ['int', 0, 6000000000]],
                    'MEAS:PNOIS': [['int', 0, 6000000000], ['int', 0, 6000000000]],
                    'MEAS:SNR': [['int', 0, 6000000000], ['int', 0, 6000000000]],
                    'MEAS:3DB': [],
                    'MEAS:AM': [['int', 0, 6000000000], ['int', 3000, 10000]],
                    'MEAS:FM': [['int', 0, 6000000000], ['int', 1000, 2500]],
                    'MEAS:THD': [],
                    'MEAS:CHPOW': [['int', 0, 6000000000], ['int', 0, 6000000000]],
                    'MEAS:LINE': [],
                    'MEAS:TNF': [['int', 0, 6000000000]],
                    'MEAS:ANF': [['int', 0, 6000000000]],

                     # CONFiguration Subsystem
                     'CONF:CAPT': [],
                     'CONF:CALC': [['str', 'off', 'minh', 'maxh', 'maxd', 'aver4' , 'aver16' , 'quasip']],
                     'CONF:CORR:LOW': [['int', 0, 19], ['int', 0, 800000000], ['float', -200.0, 13.0]],
                     'CONF:CORR:HIGH': [['int', 0, 19], ['int', 0, 800000000], ['float', -200.0, 13.0]],
                     'CONF:CORR:LNA': [['int', 0, 19], ['int', 0, 800000000], ['float', -200.0, 13.0]],
                     'CONF:ULTRA:ON': [['int', 4321]],
                     'CONF:ULTRA:OFF': [],
                     

                    }

