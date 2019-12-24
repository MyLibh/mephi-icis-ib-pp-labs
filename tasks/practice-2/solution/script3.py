"""
gets() reads a line from stdin into the buffer pointed to by s until either a terminating newline or EOF, 
which it replaces with a null byte ('\0').  
No check for buffer overrun is performed (see BUGS below).

Нерешаемый таск, так как используется gets, который кладет в конце '\0', поэтому ничего прочитать не можем(только погадить)
"""