PROGRAM OperatorPrecedencePparsing;
// Прототип этой программы создан еще в 1988 году
{$APPTYPE CONSOLE}
uses
SysUtils;
CONST
    marker = '$';
    blank = ' ';
    max = 1000;
    error_msg : array['1'..'4'] of string = (
        'отсутствует операнд.',
        'несбалансированная правая скобка.',
        'отсутствует оператор.',
        'отсутствует правая скобка.' 
    );
TYPE
// Терминальные символы грамматики
    symbol = (_atom, _not, _and, _or, _imp, _equ, _lpar, _rpar, _doll);
VAR
    // Матрица отношений операторного предшествования
    matrix: ARRAY[symbol, symbol] OF char= (
    //     |    atm not and or  imp equ lp  rp  dol
    // ----+---------------------------------------
    { atm  | } ('3','>','>','>','>','>','3','>','>'),
    { not  | } ('<','<','>','>','>','>','<','>','>'),
    { and  | } ('<','<','>','>','>','>','<','>','>'),
    { or   | } ('<','<','<','>','>','>','<','>','>'),
    { imp  | } ('<','<','<','<','>','>','<','>','>'),
    { equ  | } ('<','<','<','<','<','>','<','>','>'),
    { lp   | } ('<','<','<','<','<','<','<','=','4'),
    { rp   | } ('3','>','>','>','>','>','3','>','>'),
    { dol  | } ('<','<','<','<','<','<','<','2','1') );
    s : ARRAY[0..max] OF char; // Стек разбора
    t : integer; // Указатель (индекс) вершины стека
    symbols : ARRAY[char] OF symbol;
    ch : char;
    flag, done : boolean;
    i, n : integer;
    prn : ARRAY[1..max] OF char;

PROCEDURE getch;
BEGIN
    REPEAT
        read(ch)
    UNTIL ch > blank;
END; // OF PROCEDURE 'getch'

PROCEDURE gen_prn(c: char);
BEGIN
    IF NOT (c IN ['(',')']) THEN
    BEGIN
        inc(n);
        prn[n] := c
    END
END; // OF PROCEDURE 'gen_prn'

BEGIN
    // Инициализация матрицы операторного предшествования 'matrix'

    FOR ch := chr(0) TO chr(255) DO
        IF ch IN ['A'..'Z','a'..'z','0','1'] THEN 
            symbols[ch] := _atom
        ELSE
        CASE ch OF
            '~' : symbols[ch] := _not;
            '&' : symbols[ch] := _and;
            '|' : symbols[ch] := _or;
            '>' : symbols[ch] := _imp;
            '=' : symbols[ch] := _equ;
            '(' : symbols[ch] := _lpar;
            ')' : symbols[ch] := _rpar;
            '$' : symbols[ch] := _doll;
        ELSE // Иначе
            symbols[ch] := _doll;
        END; // CASE
    done := false;
    flag := false;
    REPEAT
        writeln('ВВЕДИТЕ ИНФИКСНОЕ ВЫРАЖЕНИЕ(в конце выражения ''$''; только    ''$'' -выход)');
        n := 0;
        getch;
        IF ch = marker THEN 
            done := true
        ELSE
        BEGIN
            ///////////////////////
            /////////////////////////////////////
            // Начало'operator precedence parsing algorithm'
            s[0] := marker;
            t := 0;
            WHILE (t > 0) OR (ch <> marker) DO
            BEGIN
                CASE matrix[symbols[s[t]], symbols[ch]] OF
                '<', '=' :
                    BEGIN // Перенос
                        inc(t);
                        s[t] := ch;
                        getch;
                    END;
                '>' :
                    BEGIN // Свертка
                        REPEAT
                            gen_prn(s[t]);
                            dec(t);
                        UNTIL matrix[symbols[s[t]], symbols[s[t+1]]] = '<'
                    END;
                ELSE // Иначе
                    BEGIN
                        writeln('ОШИБКА: ' + error_msg[matrix[symbols[s[t]], symbols[ch]]]);
                        readln;
                        flag := true;
                        break; // Реализация панического анализатора
                    END;
                END; // CASE
            END; // WHILE
            // Конец 'operator precedence parsing algorithm'
            ////////////////////////////////////////////////////////////

            IF flag THEN 
                flag := false
            ELSE
            BEGIN
                write;
                ('ПОСТФИКСНАЯ ЗАПИСЬ: ');
                FOR i := 1 TO n DO write(prn[i]);
                writeln;
            END; // ELSE        
        END; // ELSE

    UNTIL done;
    readln;
END. // OF PROGRAM OperatorPrecedenceParser