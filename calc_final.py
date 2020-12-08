#PROJECT : CALCULATOR (USING TKINTER GUI)

#Modules used
import tkinter as tk
import tkinter.font as tkFont
from functools import partial
from decimal import *
import re

#Setting precision of Decimal() numbers
getcontext().prec = 11

#FLAGS
equal_flag = False
operator_flag = False
un_flag = False

#Creating Tk() object (window)
window = tk.Tk()
window.title('Calculator')

window.resizable(0,0)

#Creating font object for buttons
font = tkFont.Font(family="Segoe UI",size=15)#,weight="bold"


#DEFINING COMMAND FUNCTIONS FOR BUTTONS

#Command functions for digits, point and plus-minus operator 
#Command Function for 'btn_0'
def fn_btn_0():
    if lbl_display1['text'] == 'Undefined':
        lbl_display1['text'] = '0'
        lbl_display2['text'] = ''
        return
    
    str_value = lbl_display1['text']
    #int_value = int( lbl_display1['text'] )
    global operator_flag
    global equal_flag
    

    if equal_flag or operator_flag:
        lbl_display1['text'] = '0'
        operator_flag = False
        equal_flag = False
        
    elif str_value != '0' and len(str_value) < 11:
        lbl_display1['text'] = lbl_display1['text'] + '0'

#Command Function for 'btn_1' to 'btn_9'
def fn_btn_dig(num):
    if lbl_display1['text'] == 'Undefined':
        lbl_display1['text'] = '0'
        lbl_display2['text'] = ''
        return
    
    str_value = lbl_display1['text']
    #int_value = int( lbl_display1['text'] )
    global operator_flag
    global equal_flag
    global un_flag
    
    if equal_flag or operator_flag or un_flag:
        if equal_flag or un_flag:
            lbl_display2['text'] = ''
        lbl_display1['text'] = str(num)
        operator_flag = False
        equal_flag = False
        un_flag = False
        
    elif len(str_value) < 11 :
        if str_value == '0':
            lbl_display1['text'] = str(num)
        else:
            lbl_display1['text'] = lbl_display1['text'] + str(num)

#Command Function for 'btn_point'
def fn_btn_point():
    if lbl_display1['text'] == 'Undefined':
        lbl_display1['text'] = '0'
        lbl_display2['text'] = ''
        return
    
    str_value = lbl_display1['text']
    #int_value = int( lbl_display1['text'] )
    global operator_flag
    global equal_flag
    
    if equal_flag or operator_flag:
        lbl_display2['text'] = ''
        lbl_display1['text'] = '0.'
        operator_flag = False
        equal_flag = False
        
    elif len(str_value) < 11 and '.' not in lbl_display1['text']:
        lbl_display1['text'] = lbl_display1['text'] + '.'

#Command Function for 'btn_plus_minus'
def fn_btn_plus_minus():
    if lbl_display1['text'] == 'Undefined':
        lbl_display1['text'] = '0'
        lbl_display2['text'] = ''
        return
    
    str_value = lbl_display1['text']
    #int_value = int( lbl_display1['text'] )
    global operator_flag

    if not operator_flag and str_value != '0':
        if '-' in str_value:
            lbl_display1['text'] = str_value.replace('-', '')
        else:
            lbl_display1['text'] = '-' + str_value


#Command function for arithmetic operators
def fn_btn_opr(opr):
    global equal_flag
    global operator_flag
    global un_flag
    
    if lbl_display1['text'] == 'Undefined':
        lbl_display1['text'] = '0'
        lbl_display2['text'] = ''
        return

    elif lbl_display1['text'] != '0' and (equal_flag or operator_flag or un_flag):
        lbl_display2['text'] = remove_trail_zero_str(lbl_display1['text']) +\
                               ' ' + opr + ' '
        lbl_display1['text'] = remove_trail_zero_str(lbl_display1['text'])
        equal_flag = False
        un_flag = False
        
    else:
        lbl_display2['text'] = lbl_display2['text'] +\
                               remove_trail_zero_str(lbl_display1['text']) +\
                               ' ' + opr + ' '
        lbl_display1['text'] = remove_trail_zero_str(lbl_display1['text'])
    
    operator_flag = True

#Command function for 'btn_backspace'
def fn_btn_backspace():
    global operator_flag

    if lbl_display1['text'] == 'Undefined':
        lbl_display1['text'] = '0'
        lbl_display2['text'] = ''
        return

    if not operator_flag:
        update = lbl_display1['text'][:-1]

        if update == '':
            lbl_display1['text'] = '0'
        else:
            lbl_display1['text'] = update
    

#Function to remove insignicant trailing zeroes from decimal object
def remove_trail_zero(num):
    return num.to_integral() if num == num.to_integral() else num.normalize()

#Function to remove insignicant trailing zeroes from string object
def remove_trail_zero_str(string):
    if '.' in string:
        string = string.rstrip('0')
        string = string.rstrip('.')

    return string

#Command function for 'btn_equal'
def fn_btn_equal():
    global operator_flag
    global equal_flag

    if lbl_display1['text'] == 'Undefined':
        lbl_display1['text'] = '0'
        lbl_display2['text'] = ''
        return

    if ( lbl_display1['text'] == '0' and
    ( lbl_display2['text'] == '' or lbl_display2['text'] == '0' )):
        lbl_display2['text'] = '0'
        
    elif ( lbl_display1['text'] != '0' and
    ( lbl_display2['text'] == '' or lbl_display2['text'] == '0' )):
        lbl_display2['text'] = lbl_display1['text']

    elif ( lbl_display1['text'] != '0' and
           lbl_display2['text'] == lbl_display1['text'] ):
        lbl_display2['text'] = lbl_display1['text']

    elif ( '/' in lbl_display2['text'] or
           '\N{SUPERSCRIPT TWO}' in lbl_display2['text'] or
           '\N{SQUARE ROOT}' in lbl_display2['text']):
        return

    else:
        operand1 = ''
        operand2 = ''
        eval_str = ''
        flag = False

        operands = [Decimal(x) for x in\
                re.findall(r'-?\d+\.?\d*E?\+?\d*', lbl_display2['text'])]

        operators = [x for x in re.findall(r'[+−×÷%]+ ',
                                           lbl_display2['text'])]
        
        if lbl_display2['text'][-2] == '\N{EQUALS SIGN}':
            operands[0] = Decimal( lbl_display1['text'] )
            
            lbl_display2['text'] = str(operands[0]) + ' ' +\
                                   operators[-1] +\
                                   str(operands[-1]) +\
                                   ' \N{EQUALS SIGN} '
            operands = [Decimal(x) for x in\
                re.findall(r'-?\d+\.?\d*E?\+?\d*', lbl_display2['text'])]

            operators = [x for x in re.findall(r'[+−×÷%]+ ',
                                               lbl_display2['text'])]

        else:
            operands.append( Decimal(lbl_display1['text']) )
            lbl_display2['text'] = remove_trail_zero_str(lbl_display2['text']) +\
                                   remove_trail_zero_str(lbl_display1['text']) +\
                                   ' \N{EQUALS SIGN} '


        for index in range(len(operators)):
            operators[index] = operators[index].replace('+', '+')
            operators[index] = operators[index].replace('−', '-')
            operators[index] = operators[index].replace('×', '*')
            operators[index] = operators[index].replace('÷', '/')

        try:
            if operators[0] == '% ':
                result = (operands[0] * operands[1])/100
            else:
                result = eval( repr(operands[0]) + operators[0] + repr(operands[1]) )
            result = remove_trail_zero(result)
            for index in range(1, len(operators)):
                if operators[index] == '% ':
                    result = (result * operands[index+1])/100
                else:
                    result = eval( repr(result) +\
                                   operators[index] + repr(operands[index+1]) )
                    result = remove_trail_zero(result)
        except (ZeroDivisionError, ArithmeticError):
            result = 'Undefined'

        result = result + Decimal('0')

        if Decimal('-1') < result < Decimal('1'):
            result = result.quantize(Decimal('1.000000000'))
            result = remove_trail_zero(result)
            
        if len( str(result) ) > 12:
            result = f"{result:.5E}"
        lbl_display1['text'] = str(result)

    equal_flag = True

#Command function for 'btn_C'
def fn_btn_C():
    lbl_display1['text'] = '0'
    lbl_display2['text'] = ''

#Command function for 'btn_CE'
def fn_btn_CE():
    global equal_flag
    
    if equal_flag:
        lbl_display1['text'] = '0'
        lbl_display2['text'] = ''
        equal_flag = False
    else:
        lbl_display1['text'] = '0'

#Command function for Unary oprators
def fn_btn_un(operator):
    global un_flag

    if lbl_display1['text'] == 'Undefined':
        lbl_display1['text'] = '0'
        lbl_display2['text'] = ''
        return
    
    if operator == 'inverse':
        lbl_display2['text'] = '1 / ' +\
                               remove_trail_zero_str(lbl_display1['text']) +\
                               ' = '
        result = 1/remove_trail_zero(
            Decimal(lbl_display1['text']))
        
        
        result = result.quantize(Decimal('1.00000000'))
        result = remove_trail_zero(result)
           
        if len( str(result) ) > 12:
            result = f"{result:.2E}"
        lbl_display1['text'] = str(result)
        un_flag = True
        
    elif operator == 'square':
        lbl_display2['text'] = remove_trail_zero_str(lbl_display1['text']) +\
                               '\N{SUPERSCRIPT TWO}' + ' = '
        result = remove_trail_zero(
            Decimal(lbl_display1['text'])**2)

        if Decimal('-1') < result < Decimal('1'):
            result = result.quantize(Decimal('1.000000000'))
            result = remove_trail_zero(result)
            
        if len( str(result) ) > 12:
            result = f"{result:.2E}"
        lbl_display1['text'] = str(result)
        un_flag = True

    elif operator == 'square root':
        lbl_display2['text'] = '\N{SQUARE ROOT}' +\
                               remove_trail_zero_str(lbl_display1['text']) +\
                               ' = '
        if Decimal( lbl_display1['text'] ) < 0:
            lbl_display1['text'] = 'Undefined'
            return

        result = Decimal( lbl_display1['text'] ).sqrt()

        if Decimal('-1') < result < Decimal('1'):
            result = result.quantize(Decimal('1.000000000'))
            result = remove_trail_zero(result)
            
        lbl_display1['text'] = remove_trail_zero_str( str(result) )
        un_flag = True
    



#DIGIT STRUCTURE

frm_digits = tk.Frame(
    master = window,
    bg = 'gray90',
    borderwidth = 1
    )
frm_digits.grid(row=3,column=0)

#Dict to store all digit button objects, decimal point and plus-minus operator
digits = {}
for num in range(1,10):
    digits[f'btn_{num}'] = {}

digit_list = iter( list( range(1,10) ) )

for row in range(2,-1,-1):
    for col in range(0,3):
        
        digit = next(digit_list)

        digits[f'btn_{digit}']['frm'] = tk.Frame(
            frm_digits,
            width = 80,
            height = 53
            )
        digits[f'btn_{digit}']['frm'].grid(column=col, row=row)
        digits[f'btn_{digit}']['frm'].grid_propagate(False)
        digits[f'btn_{digit}']['frm'].rowconfigure(0, weight=1)
        digits[f'btn_{digit}']['frm'].columnconfigure(0, weight=1)
        
        digits[f'btn_{digit}']['btn'] = tk.Button(
            master = digits[f'btn_{digit}']['frm'],
            text = f'{digit}',
            bg = 'snow',
            font = font
            )
        
        digits[f'btn_{digit}']['btn'].grid(
            row = 0,
            column = 0,
            padx = 1,
            pady = 1,
            sticky = 'nsew'
            )

action1 = partial(fn_btn_dig, 1)
digits['btn_1']['btn']['command'] = action1

action2 = partial(fn_btn_dig, 2)
digits['btn_2']['btn']['command'] = action2

action3 = partial(fn_btn_dig, 3)
digits['btn_3']['btn']['command'] = action3

action4 = partial(fn_btn_dig, 4)
digits['btn_4']['btn']['command'] = action4

action5 = partial(fn_btn_dig, 5)
digits['btn_5']['btn']['command'] = action5

action6 = partial(fn_btn_dig, 6)
digits['btn_6']['btn']['command'] = action6

action7 = partial(fn_btn_dig, 7)
digits['btn_7']['btn']['command'] = action7

action8 = partial(fn_btn_dig, 8)
digits['btn_8']['btn']['command'] = action8

action9 = partial(fn_btn_dig, 9)
digits['btn_9']['btn']['command'] = action9



#Adding '0' button to dict digits and frm_digits
digits[f'btn_0'] = {}
digits[f'btn_0']['frm'] = tk.Frame(
            frm_digits,
            width = 80,
            height = 53
            )

digits[f'btn_0']['frm'].grid(column=1, row=3)
digits[f'btn_0']['frm'].grid_propagate(False)
digits[f'btn_0']['frm'].rowconfigure(0, weight=1)
digits[f'btn_0']['frm'].columnconfigure(0, weight=1)
        
digits[f'btn_0']['btn'] = tk.Button(
    master = digits[f'btn_0']['frm'],
    text = f'0',
    bg = 'snow',
    font = font,
    command = fn_btn_0
    )

digits[f'btn_0']['btn'].grid(
    row = 0,
    column = 0,
    padx = 1,
    pady = 1,
    sticky = 'nsew'
    )

#Adding '.' button to dict digits and frm_digits
digits[f'btn_point'] = {}
digits[f'btn_point']['frm'] = tk.Frame(
            frm_digits,
            width = 80,
            height = 53
            )

digits[f'btn_point']['frm'].grid(column=2, row=3)
digits[f'btn_point']['frm'].grid_propagate(False)
digits[f'btn_point']['frm'].rowconfigure(0, weight=1)
digits[f'btn_point']['frm'].columnconfigure(0, weight=1)
        
digits[f'btn_point']['btn'] = tk.Button(
    master = digits[f'btn_point']['frm'],
    text = f'.',
    bg = 'snow',
    font = font,
    command = fn_btn_point
    )

digits[f'btn_point']['btn'].grid(
    row = 0,
    column = 0,
    padx = 1,
    pady = 1,
    sticky = 'nsew'
    )


#Adding 'plus-minus' button to dict digits and frm_digits
digits[f'btn_plus_minus'] = {}
digits[f'btn_plus_minus']['frm'] = tk.Frame(
            frm_digits,
            width = 80,
            height = 53
            )

digits[f'btn_plus_minus']['frm'].grid(column=0, row=3)
digits[f'btn_plus_minus']['frm'].grid_propagate(False)
digits[f'btn_plus_minus']['frm'].rowconfigure(0, weight=1)
digits[f'btn_plus_minus']['frm'].columnconfigure(0, weight=1)
        
digits[f'btn_plus_minus']['btn'] = tk.Button(
    master = digits[f'btn_plus_minus']['frm'],
    text = f'\N{PLUS-MINUS SIGN}',
    bg = 'snow',
    font = font,
    command = fn_btn_plus_minus
    )

digits[f'btn_plus_minus']['btn'].grid(
    row = 0,
    column = 0,
    padx = 1,
    pady = 1,
    sticky = 'nsew'
    )


#OPERATOR1 STRUCTURE

font_operator = tkFont.Font(family="Segoe UI",size=20)

frm_operators1 = tk.Frame(
    master = window,
    bg = 'gray90',
    borderwidth = 1
    )
frm_operators1.grid(row=2,column=1,rowspan=2)

#Dict to store all operator button objects and backspace 
operators1 = {}

#Adding 'backspace' button to dict operators1 and frm_operators1
operators1['btn_backspace'] = {}
operators1[f'btn_backspace']['frm'] = tk.Frame(
            frm_operators1,
            width = 80,
            height = 53
            )

operators1[f'btn_backspace']['frm'].grid(column=0, row=0)
operators1[f'btn_backspace']['frm'].grid_propagate(False)
operators1[f'btn_backspace']['frm'].rowconfigure(0, weight=1)
operators1[f'btn_backspace']['frm'].columnconfigure(0, weight=1)
        
operators1[f'btn_backspace']['btn'] = tk.Button(
    master = operators1[f'btn_backspace']['frm'],
    text = f'\N{ERASE TO THE LEFT}',
    bg = '#ebeef0',
    font = font,
    command = fn_btn_backspace
    )

operators1[f'btn_backspace']['btn'].grid(
    row = 0,
    column = 0,
    padx = 1,
    pady = 1,
    sticky = 'nsew'
    )

#Adding 'division' button to dict operators1 and frm_operators1
operators1['btn_div'] = {}
operators1[f'btn_div']['frm'] = tk.Frame(
            frm_operators1,
            width = 80,
            height = 53
            )

operators1[f'btn_div']['frm'].grid(column=0, row=1)
operators1[f'btn_div']['frm'].grid_propagate(False)
operators1[f'btn_div']['frm'].rowconfigure(0, weight=1)
operators1[f'btn_div']['frm'].columnconfigure(0, weight=1)

action_div = partial(fn_btn_opr, '\N{DIVISION SIGN}')

operators1[f'btn_div']['btn'] = tk.Button(
    master = operators1[f'btn_div']['frm'],
    text = f'\N{DIVISION SIGN}',
    bg = '#ebeef0',
    font = font_operator,
    command = action_div
    )

operators1[f'btn_div']['btn'].grid(
    row = 0,
    column = 0,
    padx = 1,
    pady = 1,
    sticky = 'nsew'
    )

#Adding 'multiplication' button to dict operators1 and frm_operators1
operators1['btn_mult'] = {}
operators1[f'btn_mult']['frm'] = tk.Frame(
            frm_operators1,
            width = 80,
            height = 53
            )

operators1[f'btn_mult']['frm'].grid(column=0, row=2)
operators1[f'btn_mult']['frm'].grid_propagate(False)
operators1[f'btn_mult']['frm'].rowconfigure(0, weight=1)
operators1[f'btn_mult']['frm'].columnconfigure(0, weight=1)

action_mult = partial(fn_btn_opr, '\N{MULTIPLICATION SIGN}')

operators1[f'btn_mult']['btn'] = tk.Button(
    master = operators1[f'btn_mult']['frm'],
    text = f'\N{MULTIPLICATION SIGN}',
    bg = '#ebeef0',
    font = font_operator,
    command = action_mult
    )

operators1[f'btn_mult']['btn'].grid(
    row = 0,
    column = 0,
    padx = 1,
    pady = 1,
    sticky = 'nsew'
    )

#Adding 'addition' button to dict operators1 and frm_operators1
operators1['btn_add'] = {}
operators1[f'btn_add']['frm'] = tk.Frame(
            frm_operators1,
            width = 80,
            height = 53
            )

operators1[f'btn_add']['frm'].grid(column=0, row=3)
operators1[f'btn_add']['frm'].grid_propagate(False)
operators1[f'btn_add']['frm'].rowconfigure(0, weight=1)
operators1[f'btn_add']['frm'].columnconfigure(0, weight=1)

action_add = partial(fn_btn_opr, '\N{PLUS SIGN}')
        
operators1[f'btn_add']['btn'] = tk.Button(
    master = operators1[f'btn_add']['frm'],
    text = f'\N{PLUS SIGN}',
    bg = '#ebeef0',
    font = font_operator,
    command = action_add
    )

operators1[f'btn_add']['btn'].grid(
    row = 0,
    column = 0,
    padx = 1,
    pady = 1,
    sticky = 'nsew'
    )

#Adding 'subtraction' button to dict operators1 and frm_operators1
operators1['btn_sub'] = {}
operators1[f'btn_sub']['frm'] = tk.Frame(
            frm_operators1,
            width = 80,
            height = 53
            )

operators1[f'btn_sub']['frm'].grid(column=0, row=4)
operators1[f'btn_sub']['frm'].grid_propagate(False)
operators1[f'btn_sub']['frm'].rowconfigure(0, weight=1)
operators1[f'btn_sub']['frm'].columnconfigure(0, weight=1)

action_sub = partial(fn_btn_opr, '\N{MINUS SIGN}')
        
operators1[f'btn_sub']['btn'] = tk.Button(
    master = operators1[f'btn_sub']['frm'],
    text = f'\N{MINUS SIGN}',
    bg = '#ebeef0',
    font = font_operator,
    command = action_sub
    )

operators1[f'btn_sub']['btn'].grid(
    row = 0,
    column = 0,
    padx = 1,
    pady = 1,
    sticky = 'nsew'
    )

#Adding 'equal' button to dict operators1 and frm_operators1
operators1['btn_equal'] = {}
operators1[f'btn_equal']['frm'] = tk.Frame(
            frm_operators1,
            width = 80,
            height = 53
            )

operators1[f'btn_equal']['frm'].grid(column=0, row=5)
operators1[f'btn_equal']['frm'].grid_propagate(False)
operators1[f'btn_equal']['frm'].rowconfigure(0, weight=1)
operators1[f'btn_equal']['frm'].columnconfigure(0, weight=1)
        
operators1[f'btn_equal']['btn'] = tk.Button(
    master = operators1[f'btn_equal']['frm'],
    text = f'\N{EQUALS SIGN}',
    bg = '#99cde8',
    font = font_operator,
    command = fn_btn_equal
    )

operators1[f'btn_equal']['btn'].grid(
    row = 0,
    column = 0,
    padx = 1,
    pady = 1,
    sticky = 'nsew'
    )


#OPERATOR2 STRUCTURE

frm_operators2 = tk.Frame(
    master = window,
    bg = 'gray90',
    borderwidth = 1
    )
frm_operators2.grid(row=2,column=0)

#Dict to store all operator2 button objects 
operators2 = {}

#Adding 'percentage' button to dict operators2 and frm_operators2
operators2['btn_per'] = {}
operators2[f'btn_per']['frm'] = tk.Frame(
            frm_operators2,
            width = 80,
            height = 53
            )

operators2[f'btn_per']['frm'].grid(column=0, row=0)
operators2[f'btn_per']['frm'].grid_propagate(False)
operators2[f'btn_per']['frm'].rowconfigure(0, weight=1)
operators2[f'btn_per']['frm'].columnconfigure(0, weight=1)
        
action_per = partial(fn_btn_opr, '%')

operators2[f'btn_per']['btn'] = tk.Button(
    master = operators2[f'btn_per']['frm'],
    text = f'\N{COMMERCIAL MINUS SIGN}',
    bg = '#ebeef0',
    font = font,
    command = action_per
    )

operators2[f'btn_per']['btn'].grid(
    row = 0,
    column = 0,
    padx = 1,
    pady = 1,
    sticky = 'nsew'
    )

#Adding 'CE' button to dict operators2 and frm_operators2
operators2['btn_CE'] = {}
operators2[f'btn_CE']['frm'] = tk.Frame(
            frm_operators2,
            width = 80,
            height = 53
            )

operators2[f'btn_CE']['frm'].grid(column=1, row=0)
operators2[f'btn_CE']['frm'].grid_propagate(False)
operators2[f'btn_CE']['frm'].rowconfigure(0, weight=1)
operators2[f'btn_CE']['frm'].columnconfigure(0, weight=1)
        
operators2[f'btn_CE']['btn'] = tk.Button(
    master = operators2[f'btn_CE']['frm'],
    text = f'CE',
    bg = '#ebeef0',
    font = font,
    command = fn_btn_CE
    )

operators2[f'btn_CE']['btn'].grid(
    row = 0,
    column = 0,
    padx = 1,
    pady = 1,
    sticky = 'nsew'
    )

#Adding 'C' button to dict operators2 and frm_operators2
operators2['btn_C'] = {}
operators2[f'btn_C']['frm'] = tk.Frame(
            frm_operators2,
            width = 80,
            height = 53
            )

operators2[f'btn_C']['frm'].grid(column=2, row=0)
operators2[f'btn_C']['frm'].grid_propagate(False)
operators2[f'btn_C']['frm'].rowconfigure(0, weight=1)
operators2[f'btn_C']['frm'].columnconfigure(0, weight=1)
        
operators2[f'btn_C']['btn'] = tk.Button(
    master = operators2[f'btn_C']['frm'],
    text = f'C',
    bg = '#ebeef0',
    font = font,
    command = fn_btn_C
    )

operators2[f'btn_C']['btn'].grid(
    row = 0,
    column = 0,
    padx = 1,
    pady = 1,
    sticky = 'nsew'
    )

#Adding 'inverse' button to dict operators2 and frm_operators2
operators2['btn_inv'] = {}
operators2[f'btn_inv']['frm'] = tk.Frame(
            frm_operators2,
            width = 80,
            height = 53
            )

operators2[f'btn_inv']['frm'].grid(column=0, row=1)
operators2[f'btn_inv']['frm'].grid_propagate(False)
operators2[f'btn_inv']['frm'].rowconfigure(0, weight=1)
operators2[f'btn_inv']['frm'].columnconfigure(0, weight=1)

action_inv = partial(fn_btn_un, 'inverse')
        
operators2[f'btn_inv']['btn'] = tk.Button(
    master = operators2[f'btn_inv']['frm'],
    text = f'1/\N{MATHEMATICAL ITALIC SMALL X}',
    bg = '#ebeef0',
    font = font,
    command = action_inv
    )

operators2[f'btn_inv']['btn'].grid(
    row = 0,
    column = 0,
    padx = 1,
    pady = 1,
    sticky = 'nsew'
    )

#Adding 'square' button to dict operators2 and frm_operators2
operators2['btn_sq'] = {}
operators2[f'btn_sq']['frm'] = tk.Frame(
            frm_operators2,
            width = 80,
            height = 53
            )

operators2[f'btn_sq']['frm'].grid(column=1, row=1)
operators2[f'btn_sq']['frm'].grid_propagate(False)
operators2[f'btn_sq']['frm'].rowconfigure(0, weight=1)
operators2[f'btn_sq']['frm'].columnconfigure(0, weight=1)

action_sq = partial(fn_btn_un, 'square')
        
operators2[f'btn_sq']['btn'] = tk.Button(
    master = operators2[f'btn_sq']['frm'],
    text = f'\N{MATHEMATICAL ITALIC SMALL X}\N{SUPERSCRIPT TWO}',
    bg = '#ebeef0',
    font = font,
    command = action_sq
    )

operators2[f'btn_sq']['btn'].grid(
    row = 0,
    column = 0,
    padx = 1,
    pady = 1,
    sticky = 'nsew'
    )

#Adding 'square root' button to dict operators2 and frm_operators2
operators2['btn_sq_root'] = {}
operators2[f'btn_sq_root']['frm'] = tk.Frame(
            frm_operators2,
            width = 80,
            height = 53
            )

operators2[f'btn_sq_root']['frm'].grid(column=2, row=1)
operators2[f'btn_sq_root']['frm'].grid_propagate(False)
operators2[f'btn_sq_root']['frm'].rowconfigure(0, weight=1)
operators2[f'btn_sq_root']['frm'].columnconfigure(0, weight=1)

action_sq_root = partial(fn_btn_un, 'square root')
        
operators2[f'btn_sq_root']['btn'] = tk.Button(
    master = operators2[f'btn_sq_root']['frm'],
    text = f'\N{SQUARE ROOT}\N{MATHEMATICAL ITALIC SMALL X}',
    bg = '#ebeef0',
    font = font,
    command = action_sq_root
    )

operators2[f'btn_sq_root']['btn'].grid(
    row = 0,
    column = 0,
    padx = 1,
    pady = 1,
    sticky = 'nsew'
    )


#DISPLAY1 STRUCTURE

font_display1 = tkFont.Font(family="Segoe UI Semibold",size=35)

frm_display1 = tk.Frame(
    master = window,
    width = 320,
    #bg = 'gray90',
    borderwidth = 1
    )
frm_display1.grid(row=1,column=0,columnspan=2,sticky='ew')#columnspan=2,sticky='nsew'

lbl_display1 = tk.Label(
    master = frm_display1,
    text = '0',
    width = 11,
    #bg = 'blue',
    font = font_display1,
    #height = 10,
    anchor = 'e'
    )

lbl_display1.grid(row = 0,column = 0,sticky='e')

frm_display1.grid_rowconfigure(0, weight=1)
frm_display1.grid_columnconfigure(0, weight=1)
        
    
#DISPLAY2 STRUCTURE

font_display2 = tkFont.Font(family="Segoe UI Semilight",size=15)

frm_display2 = tk.Frame(
    master = window,
    width = 320,
    #bg = 'gray90',
    borderwidth = 1
    )
frm_display2.grid(row=0,column=0,columnspan=2,sticky='ew')#columnspan=2,sticky='nsew'

lbl_display2 = tk.Label(
    master = frm_display2,
    #text = '0123+-',
    #width = 11,
    #bg = 'blue',
    font = font_display2,
    #height = 10
    )

lbl_display2.grid(row = 0,column = 0,sticky='e')

frm_display2.grid_rowconfigure(0, weight=1)
frm_display2.grid_columnconfigure(0, weight=1)


window.mainloop()

