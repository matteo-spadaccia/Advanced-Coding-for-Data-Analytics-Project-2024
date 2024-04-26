def section(x:str):
  '''
  Function to clearly depict sections of output
  - - -
  Inputs:
    x: a sting containing any text to display as section title or one of the section-end keywords (i.e., 'done' or 'end')
  Outputs:
    None (only printings enacted)
  - - -
  '''
  
  if x.lower() == 'done':
    print('_'*74+" DONE!\n\n")
  elif x.lower() == 'end':
    print('_'*80+"\n\n")
  else:
    print(x+' '+'_'*(79-len(x)))